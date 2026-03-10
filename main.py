import logging
import os
from telethon import TelegramClient, events

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# রেলওয়ে Variables থেকে তথ্য নেওয়া
API_ID = int(os.getenv("API_ID")) 
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("TOKEN")
CHANNEL_USERNAME = "shibir_online_library"

# ক্লায়েন্ট সেটআপ
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন, আমি সরাসরি বইটির লিঙ্ক খুঁজে দেব।")

@client.on(events.NewMessage)
async def search_books(event):
    # কমান্ড বা নিজের মেসেজ হলে ইগনোর করবে
    if event.text.startswith('/') or event.is_group: return
    
    query = event.text
    if len(query) < 2:
        await event.reply("অনুগ্রহ করে বইয়ের নাম একটু বিস্তারিত লিখুন।")
        return

    # সার্চিং নোটিফিকেশন
    search_msg = await event.reply("🔍 আমাদের লাইব্রেরিতে বইটি খুঁজছি...")
    
    found = False
    # চ্যানেলের মেসেজ সার্চ করা
    async for message in client.iter_messages(CHANNEL_USERNAME, search=query, limit=5):
        found = True
        # সরাসরি মেসেজের লিঙ্ক তৈরি (যেমন: t.me/channel/123)
        msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
        
        # মেসেজের প্রথম কিছু অংশ দেখানো যাতে ইউজার বুঝতে পারে
        snippet = message.text[:150] if message.text else "বইটির পোস্ট দেখতে নিচের লিঙ্কে ক্লিক করুন।"
        
        response = (
            f"📖 **আপনার কাঙ্ক্ষিত বইয়ের লিঙ্ক:**\n\n"
            f"📄 {snippet}...\n\n"
            f"🔗 [সরাসরি এখানে ক্লিক করুন]({msg_link})"
        )
        await event.reply(response, link_preview=True)
        break # প্রথম ভালো রেজাল্ট পেলেই থেমে যাবে

    if not found:
        await event.reply("❌ দুঃখিত, এই নামে কোনো বই আমাদের চ্যানেলে পাওয়া যায়নি।")
    
    await search_msg.delete()

print("বটটি এখন সক্রিয়...")
client.run_until_disconnected()
