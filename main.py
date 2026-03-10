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

# -------- Index Channel --------
async def index_channel():
    print("📚 Channel indexing started")

    count = 0

    async for message in client.iter_messages(CHANNEL_ID, limit=3000):

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

        count += 1

        if count % 200 == 0:
            print(f"Indexed {count} messages")

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

        text += f"📖 {r['name'][:40]}...\n🔗 {link}\n\n"

    await event.reply(text, link_preview=False)


# -------- Send PDF --------
@client.on(events.NewMessage(pattern="/pdf"))
async def send_pdf(event):

    if not event.is_private:
        return

    try:
        msg_id = int(event.text.split(" ")[1])

        await client.forward_messages(
            event.chat_id,
            msg_id,
            CHANNEL_ID
        )

    except:
        await event.reply("ব্যবহার: /pdf message_id")


# -------- Main --------
async def main():

    await client.start(bot_token=BOT_TOKEN)

    print("🤖 Bot started")

    # indexing background এ চলবে
    asyncio.create_task(index_channel())

    await client.run_until_disconnected()


asyncio.run(main())
