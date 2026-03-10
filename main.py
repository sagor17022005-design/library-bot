import logging
import os
import asyncio
from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()

# আপনার সঠিক চ্যানেল আইডি
CHANNEL_ID = -1001003525284401 

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের সঠিক নাম লিখুন।")

@client.on(events.NewMessage)
async def search_and_send(event):
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip().lower()
    search_msg = await event.reply("🔍 পুরো লাইব্রেরি গভীরভাবে স্ক্যান করছি... একটু সময় দিন।")
    
    found_count = 0
    try:
        # শেষ ৩০০০ মেসেজ পর্যন্ত স্ক্যান করবে
        async for message in client.iter_messages(CHANNEL_ID, limit=3000):
            # মেসেজের টেক্সট সংগ্রহ
            msg_text = (message.text or "").lower()
            
            # ফাইলের নাম সংগ্রহ (যদি থাকে)
            file_name = ""
            if message.file and message.file.name:
                file_name = message.file.name.lower()
            
            # যদি টেক্সট অথবা ফাইলের নামের মধ্যে আপনার লেখা শব্দটি থাকে
            if query in msg_text or query in file_name:
                found_count += 1
                await client.forward_messages(event.chat_id, message)
                if found_count >= 5: # সর্বোচ্চ ৫টি রেজাল্ট
                    break 

    except Exception as e:
        logging.error(f"Error: {e}")

    if found_count == 0:
        await event.reply(f"❌ দুঃখিত, '{query}' শব্দটি টেক্সট বা ফাইলের নামের কোথাও খুঁজে পাওয়া যায়নি।")
    
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is ready for deep scan!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
