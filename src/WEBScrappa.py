import requests
from bs4 import BeautifulSoup

def get_exchange_rates() -> dict:
    url = "https://www.cbr.ru/currency_base/daily/"
    response = requests.get(url)

    if response.status_code != 200:
        return "Не удалось получить данные с сайта."

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="data")

    if not table:
        return "Таблица с курсами валют не найдена."

    exchange_rates = {}

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) >= 5:
            currency_code = cells[1].text.strip()
            currency_amount = float(cells[2].text.strip())
            currency_definition = cells[3].text.strip()
            currency_rate = float(cells[4].text.replace(",", ".").strip())
            exchange_rates[currency_code] = (currency_definition, currency_rate, currency_amount)

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
    exchange_rates = get_exchange_rates()

    print("Сортировка по коду валюты (по возрастанию):")
    print(sort_by_code(exchange_rates, ascending=True))

    print("Сортировка по коду валюты (по убыванию):")
    print(sort_by_code(exchange_rates, ascending=False))

    print("Сортировка по определению валюты (по возрастанию):")
    print(sort_by_definition(exchange_rates, ascending=True))

    print("Сортировка по определению валюты (по убыванию):")
    print(sort_by_definition(exchange_rates, ascending=False))

    print("Сортировка по курсу валюты (по возрастанию):")
    print(sort_by_rate(exchange_rates, ascending=True))

    print("Сортировка по курсу валюты (по убыванию):")
    print(sort_by_rate(exchange_rates, ascending=False))