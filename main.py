import logging
import os
import asyncio
import firebase_admin
from firebase_admin import credentials, db
from telethon import TelegramClient, events

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# এনভায়রনমেন্ট ভেরিয়েবল (রেলওয়ে থেকে আসবে)
API_ID = int(os.getenv("API_ID").strip())
API_HASH = os.getenv("API_HASH").strip()
BOT_TOKEN = os.getenv("TOKEN").strip()

# ১. ফায়ারবেস সেটআপ
# নিশ্চিত করুন firebase-key.json ফাইলটি main.py এর পাশে আছে
try:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://librarybot-f2e86-default-rtdb.firebaseio.com/'
    })
except Exception as e:
    logging.error(f"ফায়ারবেস কানেকশন এরর: {e}")

client = TelegramClient('bot_session', API_ID, API_HASH)

# ২. অটোমেটিক বই সেভ করার ফাংশন (অ্যাডমিনদের জন্য)
# এটি আপনার চ্যানেলে নতুন কোনো ফাইল আসলে সেটি নিজে নিজেই ডেটাবেসে সেভ করবে
@client.on(events.NewMessage(func=lambda e: e.is_channel or e.is_group))
async def auto_save_books(event):
    if event.document:
        # ফাইলের নাম সংগ্রহ করা (যদি ফাইলে নাম না থাকে তবে মেসেজ টেক্সট নেওয়া হবে)
        file_name = ""
        if event.message.message:
            file_name = event.message.message
        else:
            for attr in event.document.attributes:
                if hasattr(attr, 'file_name'):
                    file_name = attr.file_name
                    break
        
        if file_name:
            # টেলিগ্রাম মেসেজ লিঙ্ক তৈরি করা
            chat = await event.get_chat()
            msg_link = f"https://t.me/{chat.username}/{event.id}" if chat.username else f"https://t.me/c/{chat.id}/{event.id}"
            
            # ফায়ারবেসে সেভ করা
            ref = db.reference('books')
            ref.push({
                'name': file_name,
                'link': msg_link
            })
            logging.info(f"অটো সেভ হয়েছে: {file_name}")

# ৩. ইউজারদের জন্য সার্চ ফাংশন
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("আসসালামু আলাইকুম! আপনি যা খুঁজছেন তার নাম লিখুন, আমি ফায়ারবেস থেকে সেকেন্ডে লিঙ্ক বের করে দিচ্ছি।")

@client.on(events.NewMessage)
async def search_books(event):
    if not event.is_private or event.text.startswith('/'):
        return

    query = event.text.strip().lower()
    ref = db.reference('books')
    all_books = ref.get()

    results = []
    if all_books:
        # ডেটাবেস থেকে সার্চ করা
        data = all_books.values() if isinstance(all_books, dict) else all_books
        for book in data:
            if book and query in book.get('name', '').lower():
                results.append(f"📖 **{book['name']}**\n🔗 [সরাসরি ডাউনলোড লিঙ্ক]({book['link']})")

    if not results:
        await event.reply(f"❌ দুঃখিত, '{query}' নামে কিছু পাওয়া যায়নি।")
    else:
        response = "✅ **নিচের রেজাল্টগুলো পাওয়া গেছে:**\n\n" + "\n\n".join(results[:10])
        await event.reply(response, link_preview=False)

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("বট এখন ফায়ারবেসের সাথে সচল!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
