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
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন, আমি সরাসরি ফাইলটি পাঠিয়ে দেব ইনশাআল্লাহ।")

@client.on(events.NewMessage)
async def search_and_send_pdf(event):
    # শুধু প্রাইভেট চ্যাটে রেসপন্স করবে
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip()
    if len(query) < 2:
        await event.reply("অনুগ্রহ করে বইয়ের নাম একটু বিস্তারিত লিখুন।")
        return

    search_msg = await event.reply(f"🔍 '{query}' বইটি আমাদের লাইব্রেরিতে খুঁজছি...")
    
    found = False
    try:
        # চ্যানেল এনটিটি গেট করা
        entity = await client.get_entity(CHANNEL_USERNAME)
        
        # চ্যানেলে সার্চ করা
        async for message in client.iter_messages(entity, search=query, limit=10):
            if message.text and query.lower() in message.text.lower():
                found = True
                # ফাইলটি ডাউনলোড না করে সরাসরি ফরওয়ার্ড করা (এটি সুপার ফাস্ট)
                await client.forward_messages(event.chat_id, message)
                break 

        # যদি না পাওয়া যায় তবে ডিপ সার্চ (শেষ ৫০০ মেসেজ)
        if not found:
            async for message in client.iter_messages(entity, limit=500):
                if message.text and query.lower() in message.text.lower():
                    found = True
                    await client.forward_messages(event.chat_id, message)
                    break

    except Exception as e:
        logging.error(f"Error: {e}")
        await event.reply("⚠️ একটি সমস্যা হয়েছে। দয়া করে কিছুক্ষণ পর আবার চেষ্টা করুন।")

    if not found:
        await event.reply(f"❌ দুঃখিত, '{query}' নামে কোনো বই বা ফাইল পাওয়া যায়নি।")
    
    # "খুঁজছি" মেসেজটি ডিলিট করে দেওয়া
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is successfully running with forward mode!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
