import logging
import os
import asyncio
from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip())
BOT_TOKEN = os.getenv("TOKEN").strip()

# আপনার সঠিক চ্যানেল আইডি
CHANNEL_ID = -1001003525284401 

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখুন, আমি সরাসরি ফাইলটি দিচ্ছি।")

@client.on(events.NewMessage)
async def search_and_send(event):
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip().lower()
    search_msg = await event.reply(f"🔍 '{query}' শব্দটি লাইব্রেরিতে খুঁজছি...")
    
    found_count = 0
    scanned = 0
    
    try:
        # আমরা শেষ ২০০০টি মেসেজ চেক করব যাতে কোনো বই বাদ না পড়ে
        async for message in client.iter_messages(CHANNEL_ID, limit=2000):
            scanned += 1
            msg_text = (message.text or "").lower()
            
            # আংশিক মিল চেক করা (যাতে শুধু 'কুরআন' লিখলেই সব রেজাল্ট আসে)
            if query in msg_text:
                found_count += 1
                # সরাসরি মেসেজ ফরওয়ার্ড করা (ফাইলসহ)
                await client.forward_messages(event.chat_id, message)
                
                # যদি অনেক ফাইল পাওয়া যায়, তবে প্রথম ৫টি পাঠিয়ে থেমে যাবে যাতে জ্যাম না হয়
                if found_count >= 5:
                    break 

    except Exception as e:
        await event.reply(f"⚠️ এরর: {str(e)}")

    if found_count == 0:
        await event.reply(f"❌ দুঃখিত, '{query}' নামে কিছু পাওয়া যায়নি।\nবটটি মোট {scanned}টি মেসেজ স্ক্যান করেছে।")
    else:
        await event.reply(f"✅ মোট {found_count}টি রেজাল্ট উপরে পাঠানো হয়েছে।")
    
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is successfully running!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
