import logging
import os
import asyncio
from telethon import TelegramClient, events

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip())
BOT_TOKEN = os.getenv("TOKEN").strip()
CHANNEL_USERNAME = "shibir_online_library" 

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন, আমি সরাসরি পিডিএফ ফাইলটি পাঠিয়ে দেব ইনশাআল্লাহ।")

@client.on(events.NewMessage)
async def search_and_send_pdf(event):
    if event.is_private and not event.text.startswith('/'):
        query = event.text.strip()
        if len(query) < 2:
            await event.reply("অনুগ্রহ করে বইয়ের নাম একটু বিস্তারিত লিখুন।")
            return

        search_msg = await event.reply(f"🔍 '{query}' বইটি আমাদের লাইব্রেরিতে খুঁজছি...")
        
        found = False
        try:
            entity = await client.get_entity(CHANNEL_USERNAME)
            
            # চ্যানেলে সার্চ করা
            async for message in client.iter_messages(entity, search=query, limit=15):
                # যদি মেসেজে টেক্সট থাকে এবং তাতে কুয়েরিটি থাকে
                if message.text and query.lower() in message.text.lower():
                    found = True
                    
                    # যদি মেসেজে কোনো ফাইল/মিডিয়া থাকে
                    if message.media:
                        await event.reply(f"✅ বই পাওয়া গেছে! সরাসরি ফাইলটি পাঠানো হচ্ছে...")
                        # সরাসরি ফাইলটি ফরওয়ার্ড বা সেন্ড করা
                        await client.send_file(event.chat_id, message.media, caption=f"📚 **{query}**\n\nVia: @shibir_online_library")
                    else:
                        # যদি শুধু টেক্সট থাকে তবে লিঙ্ক দেবে
                        msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
                        await event.reply(f"✅ বইয়ের পোস্ট পাওয়া গেছে, কিন্তু কোনো ফাইল নেই।\n🔗 [পোস্ট লিঙ্ক]({msg_link})")
                    break 

            # যদি সাধারণ সার্চে না পাওয়া যায় (Deep Search)
            if not found:
                async for message in client.iter_messages(entity, limit=300):
                    if message.text and query.lower() in message.text.lower():
                        found = True
                        if message.media:
                            await client.send_file(event.chat_id, message.media, caption=f"📚 **{query}** (Deep Search)")
                        else:
                            msg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
                            await event.reply(f"✅ লিঙ্ক পাওয়া গেছে: {msg_link}")
                        break

        except Exception as e:
            logging.error(f"Error: {e}")

        if not found:
            await event.reply(f"❌ দুঃখিত, '{query}' নামে কোনো বই বা ফাইল পাওয়া যায়নি।")
        
        await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is sending PDFs now!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
