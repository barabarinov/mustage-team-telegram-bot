import sqlite3
from datetime import datetime

from app.constants import DB_PATH


TO_ESCAPE = {
    "\\",
    "_",
    "*",
    "[",
    "]",
    "(",
    ")",
    "~",
    ">",
    "#",
    "+",
    "-",
    "=",
    "|",
    "{",
    "}",
    ".",
    "!",
}


def escape(s: str) -> str:
    return "".join(map(lambda c: f"\\{c}" if c in TO_ESCAPE else c, str(s)))


class DBHandler:

    def __init__(self) -> None:
        self.connection = sqlite3.connect(DB_PATH)

    def save_to_db(self, exchange_rate: float) -> None:
        cursor = self.connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS rates (time TEXT, rate REAL)")
        datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO rates (time, rate) VALUES (?, ?)",
            (datetime_str, exchange_rate),
        )
        self.connection.commit()
        self.connection.close()
