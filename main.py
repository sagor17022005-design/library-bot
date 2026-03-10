import logging
import os
import asyncio
from telethon import TelegramClient, events

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# রেলওয়ে Variables থেকে তথ্য নেওয়া
# এখানে int() ব্যবহার করা হয়েছে যাতে বড় সংখ্যা হলেও সমস্যা না হয়
API_ID = int(os.getenv("API_ID").strip()) 
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()
CHANNEL_USERNAME = "shibir_online_library"

# ক্লায়েন্ট সেটআপ
client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন, আমি সরাসরি বইটির লিঙ্ক খুঁজে দেব।")

@client.on(events.NewMessage)
async def search_books(event):
    if event.text.startswith('/') or event.is_group: return
    
    query = event.text
    if len(query) < 2:
        await event.reply("অনুগ্রহ করে বইয়ের নাম একটু বিস্তারিত লিখুন।")
        return

    search_msg = await event.reply("🔍 আমাদের লাইব্রেরিতে বইটি খুঁজছি...")
    
    found = False
    async for message in client.iter_messages(CHANNEL_USERNAME, search=query, limit=5):
        found = True
        msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
        snippet = message.text[:150] if message.text else "বইটির পোস্ট দেখতে নিচের লিঙ্কে ক্লিক করুন।"
        
        response = (
            f"📖 **আপনার কাঙ্ক্ষিত বইয়ের লিঙ্ক:**\n\n"
            f"📄 {snippet}...\n\n"
            f"🔗 [সরাসরি এখানে ক্লিক করুন]({msg_link})"
        )
        await event.reply(response, link_preview=True)
        break

    if not found:
        await event.reply("❌ দুঃখিত, এই নামে কোনো বই আমাদের চ্যানেলে পাওয়া যায়নি।")
    
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("বটটি এখন সক্রিয়...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
