import logging
import os
import asyncio
from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("TOKEN")

CHANNEL_ID = -1003525284401
CHANNEL_USERNAME = "shibir_online_library"

client = TelegramClient("library_bot", API_ID, API_HASH)

books = []

# -------- Channel Index --------
async def index_channel():
    print("📚 Channel indexing শুরু...")

    async for message in client.iter_messages(CHANNEL_ID):

        text = (message.text or "").lower()
        file_name = ""

        if message.file and message.file.name:
            file_name = message.file.name.lower()

        name = text if text else file_name

        if name:
            books.append({
                "name": name,
                "id": message.id
            })

    print(f"✅ Index complete : {len(books)} books")


# -------- Auto index new post --------
@client.on(events.NewMessage(chats=CHANNEL_ID))
async def new_book(event):

    msg = event.message
    text = (msg.text or "").lower()
    file_name = ""

    if msg.file and msg.file.name:
        file_name = msg.file.name.lower()

    name = text if text else file_name

    if name:
        books.append({
            "name": name,
            "id": msg.id
        })

        print("📥 New book added")


# -------- Start command --------
@client.on(events.NewMessage(pattern="/start"))
async def start(event):

    if not event.is_private:
        return

    await event.reply(
        "আসসালামু আলাইকুম\n\n"
        "📚 বই খুঁজতে বইয়ের নাম লিখুন"
    )


# -------- Search --------
@client.on(events.NewMessage)
async def search(event):

    if not event.is_private:
        return

    if not event.text:
        return

    if event.text.startswith("/"):
        return

    query = event.text.lower()

    results = []

    for book in books:

        if query in book["name"]:
            results.append(book)

        if len(results) >= 5:
            break

    if not results:
        await event.reply("❌ এই নামে কোনো বই পাওয়া যায়নি")
        return

    text = "📚 পাওয়া গেছে:\n\n"

    for r in results:
        link = f"https://t.me/{CHANNEL_USERNAME}/{r['id']}"
        text += f"🔗 {link}\n\n"

    await event.reply(text, link_preview=False)


# -------- Main --------
async def main():

    await client.start(bot_token=BOT_TOKEN)

    await index_channel()

    print("🤖 Bot Running...")

    await client.run_until_disconnected()


asyncio.run(main())
