import logging
import os
import asyncio
from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()
CHANNEL_USERNAME = "shibir_online_library" 

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখুন, আমি সরাসরি ফাইলটি দিচ্ছি।")

@client.on(events.NewMessage)
async def search_and_send(event):
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip().lower()
    search_msg = await event.reply("🔍 লাইব্রেরি স্ক্যান করছি, একটু ধৈর্য ধরুন...")
    
    found = False
    try:
        # সরাসরি চ্যানেলের শেষ ৫০০ মেসেজ তুলে এনে চেক করা
        async for message in client.iter_messages(CHANNEL_USERNAME, limit=500):
            if message.text and query in message.text.lower():
                found = True
                # ফাইল ফরওয়ার্ড করা
                await client.forward_messages(event.chat_id, message)
                break 

    except Exception as e:
        logging.error(f"Error: {e}")
        await event.reply("⚠️ কানেকশনে সমস্যা হচ্ছে।")

    if not found:
        await event.reply(f"❌ দুঃখিত, '{query}' নামে কিছু পাওয়া যায়নি। সঠিক নাম লিখুন।")
    
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is active!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
