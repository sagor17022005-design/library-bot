import logging
import os
import asyncio
from telethon import TelegramClient, events

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()
CHANNEL_USERNAME = "shibir_online_library" 

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন, আমি ফাইলটি পাঠিয়ে দিচ্ছি ইনশাআল্লাহ।")

@client.on(events.NewMessage)
async def search_and_send(event):
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip().lower()
    search_msg = await event.reply("🔍 লাইব্রেরি স্ক্যান করছি... একটু সময় দিন।")
    
    found_count = 0
    scanned_count = 0
    
    try:
        # চ্যানেল থেকে সরাসরি মেসেজ চেক করা
        entity = await client.get_entity(CHANNEL_USERNAME)
        
        async for message in client.iter_messages(entity, limit=1000):
            scanned_count += 1
            # মেসেজে টেক্সট বা ক্যাপশন থাকলে তা চেক করবে
            msg_text = (message.text or "").lower()
            
            if query in msg_text:
                found_count += 1
                await client.forward_messages(event.chat_id, message)
                # প্রথম ৩টি রেজাল্ট পেলে থেমে যাবে (বেশি জ্যাম এড়াতে)
                if found_count >= 3:
                    break 

    except Exception as e:
        await event.reply(f"⚠️ এরর: {str(e)}")

    if found_count == 0:
        await event.reply(f"❌ দুঃখিত, '{query}' শব্দটি আমাদের শেষ ১০০০টি মেসেজে খুঁজে পাওয়া যায়নি।\n(বটটি মোট {scanned_count}টি মেসেজ স্ক্যান করেছে)")
    else:
        await event.reply(f"✅ মোট {found_count}টি রেজাল্ট পাঠানো হয়েছে।")
    
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("বটটি এখন লাইভ এবং স্ক্যানিং মুডে আছে!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
