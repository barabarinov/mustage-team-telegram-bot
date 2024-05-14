import requests
from bs4 import BeautifulSoup

from app.constants import URL
from app.handlers.utils import DBHandler


def fetch_exchange_rate() -> float:
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.find("div", class_="fxKbKc").text.strip()

    return float(text.replace(",", "."))


def update_exchange_rate_hourly() -> None:
    rate = fetch_exchange_rate()
    db_handler = DBHandler()
    db_handler.save_to_db(rate)
