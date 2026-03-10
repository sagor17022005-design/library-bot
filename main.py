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
CHANNEL_USERNAME = "shibir_online_library" # লিঙ্কের জন্য ইউজারনেম

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখুন, আমি সরাসরি ডাউনলোড লিঙ্ক দিচ্ছি।")

@client.on(events.NewMessage)
async def search_and_link(event):
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip().lower()
    search_msg = await event.reply(f"🔍 '{query}' এর লিঙ্ক খুঁজছি...")
    
    results = []
    try:
        # শেষ ২০০০ মেসেজ স্ক্যান করবে
        async for message in client.iter_messages(CHANNEL_ID, limit=2000):
            text = (message.text or "").lower()
            file_name = ""
            if message.file and message.file.name:
                file_name = message.file.name.lower()
            
            if query in text or query in file_name:
                # মেসেজ লিঙ্ক তৈরি করা
                msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
                
                # কিছু টেক্সট স্যাম্পল নেওয়া (প্রথম ৫০ অক্ষর)
                snippet = text[:50].replace('\n', ' ') if text else "বইয়ের ফাইল"
                results.append(f"📖 **{snippet}...**\n🔗 [ডাউনলোড করতে এখানে ক্লিক করুন]({msg_link})")
                
                if len(results) >= 5: # সর্বোচ্চ ৫টি লিঙ্ক দেবে
                    break 

    except Exception as e:
        logging.error(f"Error: {e}")

    if not results:
        await event.reply(f"❌ দুঃখিত, '{query}' নামে কিছু পাওয়া যায়নি।")
    else:
        # সব লিঙ্ক একসাথে একটি মেসেজে পাঠানো
        final_response = "✅ **আপনার জন্য নিচের লিঙ্কগুলো পাওয়া গেছে:**\n\n" + "\n\n".join(results)
        await event.reply(final_response, link_preview=False) # প্রিভিউ বন্ধ রাখা হয়েছে যাতে জ্যাম না লাগে
    
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("বটটি এখন লিঙ্ক দেওয়ার জন্য রেডি!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
