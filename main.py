import logging
import os
import asyncio
from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("TOKEN")

CHANNEL_ID = -1003525284401

client = TelegramClient("library_bot", API_ID, API_HASH)

books = []


# -------- Index Old Books --------
async def index_channel():

    print("📚 Indexing old books...")

    async for message in client.iter_messages(CHANNEL_ID, limit=500):

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

    print(f"✅ Indexed {len(books)} books")


# -------- Auto Index New Book --------
@client.on(events.NewMessage(chats=CHANNEL_ID))
async def auto_index(event):

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

        print("📥 New book indexed")


# -------- Start --------
@client.on(events.NewMessage(pattern="/start"))
async def start(event):

    if not event.is_private:
        return

    await event.reply(
        "আসসালামু আলাইকুম\n\n"
        "📚 বই খুঁজতে বইয়ের নাম লিখুন"
    )


# -------- Search Book --------
@client.on(events.NewMessage)
async def search(event):

    if not event.is_private:
        return

    if not event.text:
        return

    if event.text.startswith("/"):
        return

    query = event.text.lower()

    for book in books:

        if query in book["name"]:

            await client.forward_messages(
                event.chat_id,
                book["id"],
                CHANNEL_ID
            )

            return

    await event.reply("❌ এই নামে কোনো বই পাওয়া যায়নি")


# -------- Main --------
async def main():

    await client.start(bot_token=BOT_TOKEN)

    print("🤖 Bot Running...")

    # background indexing
    asyncio.create_task(index_channel())

    await client.run_until_disconnected()


asyncio.run(main())
