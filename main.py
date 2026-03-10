import logging
import os  # এটি টোকেন পড়ার জন্য দরকার
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# রেলওয়ে ভেরিয়েবল থেকে টোকেন নেওয়া
TOKEN = os.getenv("TOKEN")
CHANNEL_USERNAME = "shibir_online_library"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "আসসালামু আলাইকুম! বইয়ের নাম লিখে সার্চ দিন, আমি লাইব্রেরি থেকে সেটি খুঁজে দেব।"
    )

async def search_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    if len(query) < 2:
        await update.message.reply_text("অনুগ্রহ করে বইয়ের নাম একটু বিস্তারিত লিখুন।")
        return

    # সার্চ লিঙ্ক তৈরি
    search_url = f"https://t.me/s/{CHANNEL_USERNAME}?q={query.replace(' ', '+')}"
    
    response = (
        f"📚 *সার্চ রেজাল্ট:* {query}\n\n"
        f"নিচের লিঙ্কে ক্লিক করে বইটি দেখে নিন:\n"
        f"🔗 [বইটি এখানে দেখুন]({search_url})\n\n"
        f"ধন্যবাদ!"
    )
    await update.message.reply_text(response, parse_mode='Markdown')

def main():
    if not TOKEN:
        print("Error: TOKEN variable not found in Railway settings!")
        return

    # বট স্টার্ট
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_books))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
