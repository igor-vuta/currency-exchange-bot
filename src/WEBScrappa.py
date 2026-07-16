import logging

import requests
from bs4 import BeautifulSoup

from cache import cached
from exceptions import ExchangeRateError

logger = logging.getLogger(__name__)

CBR_URL = "https://www.cbr.ru/currency_base/daily/"
REQUEST_TIMEOUT = 15


@cached("cbr:rates")
def get_exchange_rates() -> dict:
    logger.debug("Fetching CBR rates from %s", CBR_URL)
    try:
        response = requests.get(CBR_URL, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        logger.warning("CBR request failed: %s", exc)
        raise ExchangeRateError("Не удалось получить данные с сайта ЦБ.") from exc

    if response.status_code != 200:
        logger.warning("CBR returned HTTP %s", response.status_code)
        raise ExchangeRateError(f"ЦБ вернул ошибку {response.status_code}.")

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="data")

    if not table:
        logger.warning("CBR markup changed: data table not found")
        raise ExchangeRateError("Таблица с курсами валют не найдена.")

    exchange_rates = {}

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) >= 5:
            try:
                currency_code = cells[1].text.strip()
                currency_amount = float(cells[2].text.strip())
                currency_definition = cells[3].text.strip()
                currency_rate = float(cells[4].text.replace(",", ".").strip())
            except ValueError as exc:
                logger.warning("Skipping malformed CBR row: %s", exc)
                continue
            exchange_rates[currency_code] = (currency_definition, currency_rate, currency_amount)

    if not exchange_rates:
        logger.warning("CBR parsed zero rates")
        raise ExchangeRateError("Не удалось разобрать курсы валют.")

    logger.info("Loaded %s CBR rates", len(exchange_rates))
    return exchange_rates


def sort_by_code_webscraping(exchange_rates: dict, ascending: bool = True) -> str:
    sorted_rates = dict(sorted(exchange_rates.items(), key=lambda item: item[0], reverse=not ascending))
    return format_exchange_rates(sorted_rates)

def sort_by_definition_webscraping(exchange_rates: dict, ascending: bool = True) -> str:
    sorted_rates = dict(sorted(exchange_rates.items(), key=lambda item: item[1][0], reverse=not ascending))
    return format_exchange_rates(sorted_rates)

def sort_by_rate_webscraping(exchange_rates: dict, ascending: bool = True) -> str:
    sorted_rates = dict(sorted(exchange_rates.items(), key=lambda item: item[1][1], reverse=not ascending))
    return format_exchange_rates(sorted_rates)


def format_exchange_rates(sorted_rates: dict) -> str:
    result = "За 100 российских рублей вы сможете купить:\n"
    for currency_code, (definition, rate, amo) in sorted_rates.items():
        amount = 100 * amo / rate
        result += f"{amount:.2f} {currency_code} - {definition}\n"
    return result


if __name__ == "__main__":
    try:
        exchange_rates = get_exchange_rates()
    except ExchangeRateError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)

    print("Сортировка по коду валюты (по возрастанию):")
    print(sort_by_code_webscraping(exchange_rates, ascending=True))

    print("Сортировка по коду валюты (по убыванию):")
    print(sort_by_code_webscraping(exchange_rates, ascending=False))

    print("Сортировка по определению валюты (по возрастанию):")
    print(sort_by_definition_webscraping(exchange_rates, ascending=True))

    print("Сортировка по определению валюты (по убыванию):")
    print(sort_by_definition_webscraping(exchange_rates, ascending=False))

    print("Сортировка по курсу валюты (по возрастанию):")
    print(sort_by_rate_webscraping(exchange_rates, ascending=True))

    print("Сортировка по курсу валюты (по убыванию):")
    print(sort_by_rate_webscraping(exchange_rates, ascending=False))