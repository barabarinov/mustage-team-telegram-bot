import sqlite3

import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

from app.constants import XLSX_FILE_PATH, DB_PATH
from app.parser import update_exchange_rate_hourly


async def callback_hour(context: ContextTypes.DEFAULT_TYPE) -> None:
    update_exchange_rate_hourly()

    connection = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    df = pd.read_sql("SELECT * FROM rates", connection)
    df["time"] = pd.to_datetime(df["time"])
    df["time"] = df["time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.to_excel(XLSX_FILE_PATH, index=False)

    await context.bot.send_document(
        chat_id=context.job.chat_id, document=open(XLSX_FILE_PATH, "rb")
    )


async def get_exchange_rate(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    chat_id = update.effective_chat.id
    context.job_queue.run_repeating(
        callback_hour, interval=3600, first=1, chat_id=chat_id
    )
