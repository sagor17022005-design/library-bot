import logging
import os
import asyncio
from telethon import TelegramClient, events, functions, types

# লগিং
logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()
CHANNEL_USERNAME = "shibir_online_library" 

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন।")

@client.on(events.NewMessage)
async def search_books(event):
    if event.is_private and not event.text.startswith('/'):
        query = event.text.strip()
        if len(query) < 2:
            await event.reply("অনুগ্রহ করে একটু বিস্তারিত লিখুন।")
            return

        search_msg = await event.reply(f"🔍 '{query}' বইটি খুঁজছি...")
        
        found = False
        try:
            # চ্যানেল এনটিটি গেট করা
            entity = await client.get_entity(CHANNEL_USERNAME)
            
            # সার্চ করার আধুনিক পদ্ধতি (চ্যানেলের সব মেসেজ চেক করবে)
            async for message in client.iter_messages(entity, search=query):
                # নিশ্চিত করা হচ্ছে যে মেসেজে টেক্সট আছে এবং তা সার্চের সাথে মিলছে
                if message.text and query.lower() in message.text.lower():
                    found = True
                    msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
                    
                    response = (
                        f"✅ **বই খুঁজে পাওয়া গেছে!**\n\n"
                        f"📖 **পোস্টের কিছু অংশ:**\n`{message.text[:150]}...` \n\n"
                        f"🔗 [সরাসরি বইয়ের পোস্টে যেতে এখানে ক্লিক করুন]({msg_link})"
                    )
                    await event.reply(response, link_preview=True)
                    break 

        except Exception as e:
            logging.error(f"Error: {e}")

        if not found:
            # যদি সরাসরি সার্চে না পাওয়া যায়, তবে ম্যানুয়ালি মেসেজ স্ক্যান করার চেষ্টা (Deep Search)
            await search_msg.edit("🔍 গভীর অনুসন্ধান (Deep Search) করছি...")
            async for message in client.iter_messages(entity, limit=200):
                if message.text and query.lower() in message.text.lower():
                    found = True
                    msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
                    await event.reply(f"✅ **বই পাওয়া গেছে (Deep Search):**\n\n🔗 {msg_link}", link_preview=True)
                    break

        if not found:
            await event.reply(f"❌ দুঃখিত, '{query}' নামে কোনো বই চ্যানেলে পাওয়া যায়নি। বানানে কোনো ভুল আছে কি না চেক করুন।")
        
        await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is fully active now!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
