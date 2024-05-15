import requests
from bs4 import BeautifulSoup

from app.constants import URL
from app.handlers.utils import DBHandler


class InvalidHtml(Exception):
    pass


def fetch_exchange_rate() -> float:
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    div_with_data_entity_type_3 = soup.find("div", attrs={"data-entity-type": "3"})

    if not div_with_data_entity_type_3:
        raise InvalidHtml("The attribute 'data-entity-type=3' is missing!")

    sixth_div = div_with_data_entity_type_3.find_all("div")[5]
    if not sixth_div:
        raise InvalidHtml("The HTML structure has changed!")

    text = sixth_div.text.strip()
    return float(text.replace(",", "."))


def update_exchange_rate_hourly() -> None:
    rate = fetch_exchange_rate()
    db_handler = DBHandler()
    db_handler.save_to_db(rate)
