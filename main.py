import logging
import os
import asyncio
from telethon import TelegramClient, events

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()

# আপনার দেওয়া আইডিটি এখানে বসানো হয়েছে
CHANNEL_ID = -1001003525284401 

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখুন, আমি সরাসরি ফাইলটি দিচ্ছি।")

@client.on(events.NewMessage)
async def search_and_send(event):
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip().lower()
    search_msg = await event.reply("🔍 লাইব্রেরি স্ক্যান করছি... একটু সময় দিন।")
    
    found = False
    scanned = 0
    
    try:
        # সরাসরি আইডি দিয়ে মেসেজ চেক করা (সবচেয়ে নির্ভুল পদ্ধতি)
        async for message in client.iter_messages(CHANNEL_ID, limit=1000):
            scanned += 1
            msg_text = (message.text or "").lower()
            
            if query in msg_text:
                found = True
                # ফাইল সরাসরি ফরওয়ার্ড করা
                await client.forward_messages(event.chat_id, message)
                break 

    except Exception as e:
        await event.reply(f"⚠️ এরর: {str(e)}\n\nনিশ্চিত করুন বটটি চ্যানেলে অ্যাডমিন আছে।")

    if not found:
        await event.reply(f"❌ পাওয়া যায়নি। বটটি {scanned}টি মেসেজ চেক করেছে।")
    
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is Online and Ready!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
