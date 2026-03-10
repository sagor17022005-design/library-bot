import logging
import os
import asyncio
from telethon import TelegramClient, events

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()
# চ্যানেলের ইউজারনেম (লিঙ্ক থেকে @ বা https://t.me/ বাদ দিয়ে শুধু নাম)
CHANNEL_USERNAME = "shibir_online_library" 

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন, আমি সরাসরি লিঙ্ক খুঁজে দেব।")

@client.on(events.NewMessage)
async def search_books(event):
    if event.is_private and not event.text.startswith('/'):
        query = event.text.strip()
        if len(query) < 2:
            await event.reply("অনুগ্রহ করে বইয়ের নাম একটু বিস্তারিত লিখুন।")
            return

        search_msg = await event.reply(f"🔍 '{query}' বইটি আমাদের লাইব্রেরিতে খুঁজছি...")
        
        found = False
        try:
            # প্রথমে চ্যানেলের এনটিটি (Entity) নিশ্চিত করা
            entity = await client.get_entity(CHANNEL_USERNAME)
            
            # চ্যানেলে সার্চ করা (limit বাড়িয়ে ১০ করা হয়েছে)
            async for message in client.iter_messages(entity, search=query, limit=10):
                if message.text:
                    found = True
                    msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
                    
                    # সুন্দর মেসেজ ফরম্যাট
                    response = (
                        f"✅ **বই খুঁজে পাওয়া গেছে!**\n\n"
                        f"📄 {message.text[:150]}...\n\n"
                        f"🔗 [সরাসরি বইয়ের পোস্টে যেতে এখানে ক্লিক করুন]({msg_link})"
                    )
                    await event.reply(response, link_preview=True)
                    break # প্রথম সঠিক রেজাল্ট পেলেই থেমে যাবে
        
        except Exception as e:
            logging.error(f"Search error: {e}")
            await event.reply("⚠️ একটি ত্রুটি হয়েছে, দয়া করে আবার চেষ্টা করুন।")

        if not found:
            await event.reply(f"❌ দুঃখিত, '{query}' নামে কোনো বই আমাদের চ্যানেলে পাওয়া যায়নি। সঠিক নাম দিয়ে আবার চেষ্টা করুন।")
        
        await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("বটটি এখন পুরোপুরি সক্রিয়!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
