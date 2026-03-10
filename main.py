import logging
import os
import asyncio
from telethon import TelegramClient, events

# লগিং
logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()
CHANNEL_ID = -1001003525284401 
CHANNEL_USERNAME = "shibir_online_library"

# সেশন ফাইলের নাম 'bot_session' থেকে বদলে 'library_bot' দিচ্ছি যাতে ফ্রেশ স্টার্ট হয়
client = TelegramClient('library_bot', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন, আমি ডাউনলোড লিঙ্ক খুঁজে দেব।")

@client.on(events.NewMessage)
async def search_and_link(event):
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip().lower()
    search_msg = await event.reply(f"🔍 '{query}' খুঁজছি...")
    
    results = []
    try:
        # শেষ ২০০০ মেসেজ স্ক্যান
        async for message in client.iter_messages(CHANNEL_ID, limit=2000):
            text = (message.text or "").lower()
            file_name = ""
            if message.file and message.file.name:
                file_name = message.file.name.lower()
            
            if query in text or query in file_name:
                msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
                snippet = text[:40].replace('\n', ' ') if text else "বইয়ের ফাইল"
                results.append(f"📖 **{snippet}...**\n🔗 [ডাউনলোড লিঙ্ক]({msg_link})")
                if len(results) >= 5: break 

    except Exception as e:
        logging.error(f"Error: {e}")

    if not results:
        await event.reply(f"❌ '{query}' নামে কিছু পাওয়া যায়নি।")
    else:
        response = "✅ **আপনার জন্য নিচের লিঙ্কগুলো পাওয়া গেছে:**\n\n" + "\n\n".join(results)
        await event.reply(response, link_preview=False)
    
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is alive and sending links!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
