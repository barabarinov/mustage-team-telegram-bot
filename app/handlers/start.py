from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

from app.constants import GREETING_TEXT
from app.parser import update_exchange_rate_hourly


async def callback_hour(context: ContextTypes.DEFAULT_TYPE) -> None:
    update_exchange_rate_hourly()


async def run_job_hourly(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
) -> None:
    context.job_queue.run_repeating(callback_hour, interval=3600, first=1)
    print("✅ Job started successfully!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await run_job_hourly(update=update, context=context)

    reply_markup = ReplyKeyboardMarkup([["/get_exchange_rate"]], resize_keyboard=True)

    await update.effective_message.reply_text(
        text=GREETING_TEXT.format(update.effective_user.username),
        reply_markup=reply_markup,
    )
