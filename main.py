import logging
import os
import asyncio
from telethon import TelegramClient, events

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# ভেরিয়েবলগুলো নেওয়া এবং স্পেস পরিষ্কার করা
try:
    API_ID_ENV = os.getenv("API_ID", "").strip()
    API_HASH = os.getenv("API_HASH", "").strip()
    BOT_TOKEN = os.getenv("TOKEN", "").strip()
    
    # আইডিটি সংখ্যায় রূপান্তর
    API_ID = int(API_ID_ENV) if API_ID_ENV else None
except Exception as e:
    logging.error(f"Variable Error: {e}")
    API_ID = None

CHANNEL_USERNAME = "shibir_online_library"

# সেশন ফাইলের নাম 'bot' দিলে রেলওয়েতে সুবিধা হয়
client = TelegramClient('bot', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন, আমি সরাসরি লিঙ্ক খুঁজে দেব।")

@client.on(events.NewMessage)
async def search_books(event):
    if event.is_private and not event.text.startswith('/'):
        query = event.text
        if len(query) < 2:
            await event.reply("অনুগ্রহ করে বইয়ের নাম একটু বিস্তারিত লিখুন।")
            return

        search_msg = await event.reply("🔍 আমাদের লাইব্রেরিতে বইটি খুঁজছি...")
        
        found = False
        async for message in client.iter_messages(CHANNEL_USERNAME, search=query, limit=5):
            found = True
            msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
            await event.reply(f"📖 **বই পাওয়া গেছে!**\n\n🔗 [সরাসরি পোস্টে যেতে এখানে ক্লিক করুন]({msg_link})", link_preview=True)
            break

        if not found:
            await event.reply("❌ দুঃখিত, এই নামে কোনো বই পাওয়া যায়নি।")
        
        await search_msg.delete()

async def main():
    if not API_ID or not API_HASH or not BOT_TOKEN:
        print("Variables are missing! Please check Railway settings.")
        return
        
    print("Starting bot...")
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is now online!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
