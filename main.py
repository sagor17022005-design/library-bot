import logging
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

TOKEN = os.getenv("TOKEN")
CHANNEL_USERNAME = "shibir_online_library"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম! বইয়ের নাম লিখে সার্চ দিন।")

async def search_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    if len(query) < 2:
        await update.message.reply_text("অনুগ্রহ করে বিস্তারিত লিখুন।")
        return
    search_url = f"https://t.me/s/{CHANNEL_USERNAME}?q={query.replace(' ', '+')}"
    response = f"📚 *সার্চ রেজাল্ট:* {query}\n\n🔗 [বইটি এখানে দেখুন]({search_url})"
    await update.message.reply_text(response, parse_mode='Markdown')

def main():
    if not TOKEN:
        print("TOKEN not found!")
        return

    # অ্যাপ্লিকেশন তৈরি
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_books))
    
    print("Starting bot...")
    # রেলওয়েতে এটি বেশি স্টেবল
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
