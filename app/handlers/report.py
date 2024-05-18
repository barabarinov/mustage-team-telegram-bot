import sqlite3

import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

from app.constants import XLSX_FILE_PATH, DB_PATH


async def get_exchange_rate(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    connection = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

    df = pd.read_sql("SELECT * FROM rates", connection)
    df["datetime"] = pd.to_datetime(df["datetime"])

    today = pd.Timestamp.today().normalize()
    df = df[df["datetime"].dt.date == today.date()]

    if not df.empty:
        df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
        df.to_excel(XLSX_FILE_PATH, index=False)

        await context.bot.send_document(
            chat_id=update.effective_chat.id, document=open(XLSX_FILE_PATH, "rb")
        )
        print("✅ File sent successfully!")
