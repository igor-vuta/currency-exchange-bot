# src/APIRate.py
import requests
from typing import List, Tuple
from config import CURRENCYLAYER_API_KEY


BASE_URL = "https://api.currencylayer.com/live" 

currency_names = {
      "AED": "Дирхам ОАЭ",
    "AFN": "Афгани",
    "ALL": "Албанский лек",
    "AMD": "Армянский драм",
    "ANG": "Нидерландский антильский гульден",
    "AOA": "Ангольская кванза",
    "ARS": "Аргентинское песо",
    "AUD": "Австралийский доллар",
    "AWG": "Арубанский флорин",
    "AZN": "Азербайджанский манат",
    "BAM": "Боснийская конвертируемая марка",
    "BBD": "Барбадосский доллар",
    "BDT": "Бангладешская така",
    "BGN": "Болгарский лев",
    "BHD": "Бахрейнский динар",
    "BIF": "Бурундийский франк",
    "BMD": "Бермудский доллар",
    "BND": "Брунейский доллар",
    "BOB": "Боливийский боливиано",
    "BRL": "Бразильский реал",
    "BSD": "Багамский доллар",
    "BTC": "Биткойн",
    "BTN": "Бутанский нгултрум",
    "BWP": "Ботсванская пула",
    "BYN": "Белорусский рубль",
    "BYR": "Белорусский рубль (старый)",
    "BZD": "Белизский доллар",
    "CAD": "Канадский доллар",
    "CDF": "Конголезский франк",
    "CHF": "Швейцарский франк",
    "CLF": "Условная денежная единица Чили",
    "CLP": "Чилийское песо",
    "CNY": "Китайский юань",
    "CNH": "Китайский юань (офшорный)",
    "COP": "Колумбийское песо",
    "CRC": "Коста-риканский колон",
    "CUC": "Кубинское конвертируемое песо",
    "CUP": "Кубинское песо",
    "CVE": "Кабо-Верде эскудо",
    "CZK": "Чешская крона",
    "DJF": "Франк Джибути",
    "DKK": "Датская крона",
    "DOP": "Доминиканское песо",
    "DZD": "Алжирский динар",
    "EGP": "Египетский фунт",
    "ERN": "Накфа Эритреи",
    "ETB": "Эфиопский быр",
    "EUR": "Евро",
    "FJD": "Фиджийский доллар",
    "FKP": "Фунт Фолклендских островов",
    "GBP": "Фунт стерлингов Соединенного королевства",
    "GEL": "Грузинский лари",
    "GGP": "Гернсийский фунт",
    "GHS": "Ганский седи",
    "GIP": "Гибралтарский фунт",
    "GMD": "Гамбийский даласи",
    "GNF": "Гвинейский франк",
    "GTQ": "Гватемальский кетсаль",
    "GYD": "Гайанский доллар",
    "HKD": "Гонконгский доллар",
    "HNL": "Гондурасская лемпира",
    "HRK": "Хорватская куна",
    "HTG": "Гаитянский гурд",
    "HUF": "Венгерский форинт",
    "IDR": "Индонезийская рупия",
    "ILS": "Израильский шекель",
    "IMP": "Фунт Острова Мэн",
    "INR": "Индийская рупия",
    "IQD": "Иракский динар",
    "IRR": "Иранский риал",
    "ISK": "Исландская крона",
    "JEP": "Джерсийский фунт",
    "JMD": "Ямайский доллар",
    "JOD": "Иорданский динар",
    "JPY": "Японская иена",
    "KES": "Кенийский шиллинг",
    "KGS": "Киргизский сом",
    "KHR": "Камбоджийский риель",
    "KMF": "Франк Коморских островов",
    "KPW": "Северокорейская вона",
    "KRW": "Южнокорейская вона",
    "KWD": "Кувейтский динар",
    "KYD": "Доллар Каймановых островов",
    "KZT": "Казахстанский тенге",
    "LAK": "Лаосский кип",
    "LBP": "Ливанский фунт",
    "LKR": "Шри-ланкийская рупия",
    "LRD": "Либерийский доллар",
    "LSL": "Лоти Лесото",
    "LTL": "Литовский лит",
    "LVL": "Латвийский лат",
    "LYD": "Ливийский динар",
    "MAD": "Марокканский дирхам",
    "MDL": "Молдавский лей",
    "MGA": "Малагасийский ариари",
    "MKD": "Македонский денар",
    "MMK": "Мьянманский кьят",
    "MNT": "Монгольский тугрик",
    "MOP": "Патака Макао",
    "MRU": "Мавританская угия",
    "MUR": "Маврикийская рупия",
    "MVR": "Мальдивская руфия",
    "MWK": "Малавийская квача",
    "MXN": "Мексиканское песо",
    "MYR": "Малайзийский ринггит",
    "MZN": "Мозамбикский метикал",
    "NAD": "Намибийский доллар",
    "NGN": "Нигерийская найра",
    "NIO": "Никарагуанская кордоба",
    "NOK": "Норвежская крона",
    "NPR": "Непальская рупия",
    "NZD": "Новозеландский доллар",
    "OMR": "Оманский риал",
    "PAB": "Панамский бальбоа",
    "PEN": "Перуанский соль",
    "PGK": "Кина Папуа - Новая Гвинея",
    "PHP": "Филиппинское песо",
    "PKR": "Пакистанская рупия",
    "PLN": "Польский злотый",
    "PYG": "Парагвайский гуарани",
    "QAR": "Катарский риал",
    "RON": "Румынский лей",
    "RSD": "Сербский динар",
    "RUB": "Российский рубль",
    "RWF": "Руандийский франк",
    "SAR": "Саудовский риал",
    "SBD": "Доллар Соломоновых островов",
    "SCR": "Сейшельская рупия",
    "SDG": "Суданский фунт",
    "SEK": "Шведская крона",
    "SGD": "Сингапурский доллар",
    "SHP": "Фунт Святой Елены",
    "SLE": "Леоне (Сьерра-Леоне)",
    "SLL": "Сьерра-леонский леоне",
    "SOS": "Сомалийский шиллинг",
    "SRD": "Суринамский доллар",
    "STD": "Добра Сан-Томе и Принсипи",
    "SVC": "Сальвадорский колон",
    "SYP": "Сирийский фунт",
    "SZL": "Лилангени Свазиленда",
    "THB": "Таиландский бат",
    "TJS": "Таджикский сомони",
    "TMT": "Туркменский манат",
    "TND": "Тунисский динар",
    "TOP": "Паанга Тонга",
    "TRY": "Турецкая лира",
    "TTD": "Тринидадский доллар",
    "TWD": "Тайваньский доллар",
    "TZS": "Танзанийский шиллинг",
    "UAH": "Украинская гривна",
    "UGX": "Угандийский шиллинг",
    "UYU": "Уругвайское песо",
    "UZS": "Узбекский сум",
    "VEF": "Венесуэльский боливар (старый)",
    "VES": "Венесуэльский боливар",
    "VND": "Вьетнамский донг",
    "VUV": "Вату Вануату",
    "WST": "Самоанская тала",
    "XAF": "Центральноафриканский франк",
    "XAG": "Серебро",
    "XAU": "Золото",
    "XCD": "Восточно-карибский доллар",
    "XDR": "Специальные права заимствования",
    "XOF": "Западноафриканский франк",
    "XPF": "Французский тихоокеанский франк",
    "YER": "Йеменский риал",
    "ZAR": "Южноафриканский рэнд",
    "ZMK": "Замбийская квача (старый)",
    "ZMW": "Замбийская квача",
    "ZWL": "Зимбабвийский доллар"
}

def fetch_live_quotes() -> dict:
    """Return raw JSON from currencylayer or raise a helpful error."""
    try:
        resp = requests.get(
            BASE_URL,
            params={"access_key": CURRENCYLAYER_API_KEY},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success", False):
            raise RuntimeError(f"Currencylayer error: {data.get('error', {}).get('info')}")
        return data
    except Exception as e:
        raise RuntimeError(f"Failed to fetch currencylayer quotes: {e}")

def build_rub_based_table(data: dict) -> List[Tuple[float, str, str]]:
    """
    Returns a list of tuples: [(rate_in_target_per_100_RUB, target_code, human_name), ...]
    """
    quotes = data["quotes"] 
    usd_to_rub = quotes.get("USDRUB")
    if not usd_to_rub:
        raise RuntimeError("USDRUB not present in quotes; cannot convert from RUB base")

    table = []
    for pair, usd_to_code in quotes.items():
        if not pair.startswith("USD"):
            continue
        target = pair[3:]
        human = currency_names.get(target, target)
        code_per_100_rub = (100 / usd_to_rub) * usd_to_code
        table.append((code_per_100_rub, target, human))
    return table

def sort_by_rate_api(rows: List[Tuple[float, str, str]], reverse=False) -> str:
    return format_exchange_rates(sorted(rows, key=lambda x: x[0], reverse=reverse))

def sort_by_currency_code_api(rows: List[Tuple[float, str, str]], reverse=False) -> str:
    return format_exchange_rates(sorted(rows, key=lambda x: x[1], reverse=reverse))

def sort_by_currency_name_api(rows: List[Tuple[float, str, str]], reverse=False) -> str:
    return format_exchange_rates(sorted(rows, key=lambda x: x[2], reverse=reverse))

def format_exchange_rates(sorted_rows) -> str:
    lines = ["За 100 российских рублей вы сможете купить:"]
    for amount, code, name in sorted_rows:
        lines.append(f"{amount:.2f} {code} - {name}")
    return "\n".join(lines)

def main_api_rows() -> List[Tuple[float, str, str]]:
    data = fetch_live_quotes()
    return build_rub_based_table(data)