from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from app.constants import GREETING_TEXT


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = ReplyKeyboardMarkup([["/get_exchange_rate"]], resize_keyboard=True)

    await update.effective_message.reply_text(
        text=GREETING_TEXT.format(update.effective_user.username),
        reply_markup=reply_markup,
    )
