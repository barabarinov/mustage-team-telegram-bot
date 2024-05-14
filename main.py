import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from app.handlers.report import get_exchange_rate
from app.handlers.start import start

load_dotenv()

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    TOKEN = os.getenv("TELEGRAM_TOKEN")

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_exchange_rate", get_exchange_rate))

    application.run_polling()
