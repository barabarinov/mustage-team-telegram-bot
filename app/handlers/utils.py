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
        self.connection = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        self.initialize_db()

    def initialize_db(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS rates (datetime TIMESTAMP, rate REAL)")
        self.connection.commit()

    def save_to_db(self, exchange_rate: float) -> None:
        cursor = self.connection.cursor()
        datetime_obj = datetime.now()

        cursor.execute(
            "INSERT INTO rates (datetime, rate) VALUES (?, ?)",
            (datetime_obj, exchange_rate),
        )
        self.connection.commit()
        self.connection.close()
