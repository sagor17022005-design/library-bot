import logging
import os
import asyncio
import firebase_admin
from firebase_admin import credentials, db
from telethon import TelegramClient, events

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# এনভায়রনমেন্ট ভেরিয়েবল থেকে তথ্য সংগ্রহ (রেলওয়েতে সেট করা থাকতে হবে)
API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()

# ১. ফায়ারবেস সেটআপ
# নিশ্চিত করুন আপনার .json ফাইলটির নাম 'firebase-key.json' এবং এটি main.py এর সাথেই আছে
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://librarybot-f2e86-default-rtdb.firebaseio.com/'
})

# ২. টেলিগ্রাম ক্লায়েন্ট সেটআপ
client = TelegramClient('library_bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! বইয়ের নাম লিখে মেসেজ দিন, আমি সরাসরি ডাউনলোড লিঙ্ক খুঁজে দেব।")

@client.on(events.NewMessage)
async def search_firebase(event):
    # শুধু প্রাইভেট চ্যাটে কাজ করবে এবং কমান্ডগুলো এড়িয়ে চলবে
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip().lower()
    search_msg = await event.reply(f"🔍 '{query}' শব্দটি ডেটাবেসে খুঁজছি...")
    
    results = []
    try:
        # ফায়ারবেসের 'books' রেফারেন্স থেকে ডেটা আনা
        ref = db.reference('books')
        all_books = ref.get()

        if all_books:
            # যদি ডেটাবেস লিস্ট আকারে থাকে (০, ১, ২...)
            if isinstance(all_books, list):
                for book in all_books:
                    if book and query in book.get('name', '').lower():
                        results.append(f"📖 **{book['name']}**\n🔗 [ডাউনলোড লিঙ্ক]({book['link']})")
            
            # যদি ডেটাবেস ডিকশনারি আকারে থাকে (key: value)
            elif isinstance(all_books, dict):
                for key, book in all_books.items():
                    if query in book.get('name', '').lower():
                        results.append(f"📖 **{book['name']}**\n🔗 [ডাউনলোড লিঙ্ক]({book['link']})")

    except Exception as e:
        logging.error(f"Firebase Error: {e}")
        await event.reply("⚠️ ডেটাবেস থেকে তথ্য সংগ্রহে সমস্যা হচ্ছে।")

    if not results:
        await event.reply(f"❌ দুঃখিত, '{query}' নামে কোনো বই ডেটাবেসে পাওয়া যায়নি।")
    else:
        # সব লিঙ্ক একসাথে সুন্দর করে সাজিয়ে পাঠানো
        response_text = "✅ **আপনার জন্য নিচের লিঙ্কগুলো পাওয়া গেছে:**\n\n" + "\n\n".join(results)
        await event.reply(response_text, link_preview=False)
    
    # "খুঁজছি..." মেসেজটি ডিলিট করে দেওয়া
    await search_msg.delete()

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is successfully running with Firebase!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
