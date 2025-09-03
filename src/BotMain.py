import datetime
from typing import Dict, List, Tuple
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters, PicklePersistence
)
from config import BOT_TOKEN
from WEBScrappa import get_exchange_rates
from APIRate import table_for_base as api_table_for_base

MESSAGES = {
    "en": {
        "choose_lang": "Choose your language:",
        "choose_source": "Choose data source:",
        "choose_base": "Choose your base currency:",
        "main_menu": "What would you like to do?",
        "source_web": "CBR (web scraping)",
        "source_api": "Currencylayer (API)",
        "act_rate_all": "1 {base} → all",
        "act_convert": "Convert amount",
        "settings": "Settings",
        "settings_title": "Settings",
        "set_lang": "Language",
        "set_source": "Data source",
        "set_base": "Base currency",
        "back": "← Back",
        "rates_for": "Rates for 1 {base}:",
        "sorting": "Sorting:",
        "sort_code_asc": "Code ↑",
        "sort_code_desc": "Code ↓",
        "sort_name_asc": "Name ↑",
        "sort_name_desc": "Name ↓",
        "sort_rate_asc": "Rate ↑",
        "sort_rate_desc": "Rate ↓",
        "pick_target": "Select target currency:",
        "enter_amount": "Enter amount (keypad):",
        "calc_result": "{amt} {base} = {res} {target}",
        "lang_en": "English",
        "lang_ru": "Русский",
        "ok": "OK",
        "clear": "Clear",
        "del": "⌫",
        "page": "Page {n}/{tot}",
        "unknown": "Please use the buttons below."
    },
    "ru": {
        "choose_lang": "Выберите язык:",
        "choose_source": "Выберите источник данных:",
        "choose_base": "Выберите базовую валюту:",
        "main_menu": "Что вы хотите сделать?",
        "source_web": "ЦБ РФ (web-scraping)",
        "source_api": "Currencylayer (API)",
        "act_rate_all": "1 {base} → все",
        "act_convert": "Конвертация суммы",
        "settings": "Настройки",
        "settings_title": "Настройки",
        "set_lang": "Язык",
        "set_source": "Источник данных",
        "set_base": "Базовая валюта",
        "back": "← Назад",
        "rates_for": "Курс для 1 {base}:",
        "sorting": "Сортировка:",
        "sort_code_asc": "Код ↑",
        "sort_code_desc": "Код ↓",
        "sort_name_asc": "Название ↑",
        "sort_name_desc": "Название ↓",
        "sort_rate_asc": "Курс ↑",
        "sort_rate_desc": "Курс ↓",
        "pick_target": "Выберите целевую валюту:",
        "enter_amount": "Введите сумму (клавиатура):",
        "calc_result": "{amt} {base} = {res} {target}",
        "lang_en": "English",
        "lang_ru": "Русский",
        "ok": "OK",
        "clear": "Сброс",
        "del": "⌫",
        "page": "Стр. {n}/{tot}",
        "unknown": "Пожалуйста, используйте кнопки ниже."
    }
}

DEFAULT_LANG = "ru"

def glang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", DEFAULT_LANG)

def tr(context: ContextTypes.DEFAULT_TYPE, key: str, **fmt) -> str:
    s = MESSAGES[glang(context)][key]
    return s.format(**fmt) if fmt else s

def set_lang(context: ContextTypes.DEFAULT_TYPE, code: str):
    context.user_data["lang"] = code

def set_source(context: ContextTypes.DEFAULT_TYPE, src: str):
    context.user_data["source"] = src

def set_base(context: ContextTypes.DEFAULT_TYPE, base: str):
    context.user_data["base"] = base

def get_source(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("source", None)

def get_base(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("base", None)

def cbr_table_for_base(base_code: str) -> List[Tuple[float, str, str]]:
    data = get_exchange_rates()
    def rub_per(code: str) -> float:
        definition, rate, amt = data[code]
        return rate / float(amt)
    base_rub = rub_per(base_code)
    rows: List[Tuple[float, str, str]] = []
    for code, (definition, rate, amt) in data.items():
        target_rub = rate / float(amt)
        rows.append((base_rub / target_rub, code, definition))
    rows = [(1.0, base_code, data[base_code][0]) if c==base_code else (v,c,n) for (v,c,n) in rows]
    rows.sort(key=lambda r: r[1])
    return rows

def lang_kb(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(tr(context, "lang_en"), callback_data="lang:en"),
                                 InlineKeyboardButton(tr(context, "lang_ru"), callback_data="lang:ru")]])

def source_kb(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(tr(context, "source_web"), callback_data="src:web")],
                                 [InlineKeyboardButton(tr(context, "source_api"), callback_data="src:api")]])

def main_menu_kb(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    base = get_base(context) or "—"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tr(context, "act_rate_all", base=base), callback_data="act:all")],
        [InlineKeyboardButton(tr(context, "act_convert"), callback_data="act:convert")],
        [InlineKeyboardButton(tr(context, "settings"), callback_data="menu:settings")]
    ])

def settings_kb(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    base = get_base(context) or "—"
    src = get_source(context) or "—"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tr(context,"set_lang"), callback_data="settings:lang"),
         InlineKeyboardButton(f"{tr(context,'set_source')} ({src})", callback_data="settings:source")],
        [InlineKeyboardButton(f"{tr(context,'set_base')} ({base})", callback_data="settings:base")],
        [InlineKeyboardButton(tr(context, "back"), callback_data="menu:main")],
    ])

def codes_list() -> List[str]:
    data = get_exchange_rates()
    return sorted(set(list(data.keys()) + ["USD","EUR","RUB","GBP","CNY","JPY","KZT","UAH"]))

def paged_codes_kb(context: ContextTypes.DEFAULT_TYPE, action_prefix: str, page: int = 0, per_page: int = 12) -> InlineKeyboardMarkup:
    codes = codes_list()
    total_pages = (len(codes)+per_page-1)//per_page
    page = max(0, min(page, total_pages-1))
    start = page*per_page
    chunk = codes[start:start+per_page]
    rows = []
    for i in range(0, len(chunk), 3):
        rows.append([InlineKeyboardButton(code, callback_data=f"{action_prefix}:pick:{code}") for code in chunk[i:i+3]])
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("‹", callback_data=f"{action_prefix}:page:{page-1}"))
    nav.append(InlineKeyboardButton(tr(context, "page", n=page+1, tot=total_pages), callback_data="noop"))
    if page < total_pages-1:
        nav.append(InlineKeyboardButton("›", callback_data=f"{action_prefix}:page:{page+1}"))
    rows.append(nav)
    rows.append([InlineKeyboardButton(tr(context, "back"), callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)

def sorting_kb(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tr(context,"sort_code_asc"),  callback_data="sort:code:asc"),
         InlineKeyboardButton(tr(context,"sort_code_desc"), callback_data="sort:code:desc")],
        [InlineKeyboardButton(tr(context,"sort_name_asc"),  callback_data="sort:name:asc"),
         InlineKeyboardButton(tr(context,"sort_name_desc"), callback_data="sort:name:desc")],
        [InlineKeyboardButton(tr(context,"sort_rate_asc"),  callback_data="sort:rate:asc"),
         InlineKeyboardButton(tr(context,"sort_rate_desc"), callback_data="sort:rate:desc")],
        [InlineKeyboardButton(tr(context, "back"), callback_data="menu:main")]
    ])

def numpad_kb(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("7", callback_data="pad:7"), InlineKeyboardButton("8", callback_data="pad:8"), InlineKeyboardButton("9", callback_data="pad:9")],
        [InlineKeyboardButton("4", callback_data="pad:4"), InlineKeyboardButton("5", callback_data="pad:5"), InlineKeyboardButton("6", callback_data="pad:6")],
        [InlineKeyboardButton("1", callback_data="pad:1"), InlineKeyboardButton("2", callback_data="pad:2"), InlineKeyboardButton("3", callback_data="pad:3")],
        [InlineKeyboardButton("0", callback_data="pad:0"), InlineKeyboardButton(".", callback_data="pad:."), InlineKeyboardButton(tr(context, "del"), callback_data="pad:del")],
        [InlineKeyboardButton(tr(context, "clear"), callback_data="pad:clear"), InlineKeyboardButton(tr(context, "ok"), callback_data="pad:ok")],
        [InlineKeyboardButton(tr(context, "back"), callback_data="menu:main")]
    ])

def format_table(rows: List[Tuple[float,str,str]], header: str) -> str:
    lines = [header, "", f"{'RATE (per 1 base)':>19} | {'CODE':<5} | NAME", "-"*55]
    for amt, code, name in rows[:80]:
        lines.append(f"{amt:19.6f} | {code:<5} | {name}")
    return "```\n" + "\n".join(lines) + "\n```"

def sort_rows(rows: List[Tuple[float,str,str]], sort_key: str, asc: bool) -> List[Tuple[float,str,str]]:
    keyfn = (lambda r: r[1]) if sort_key=="code" else ((lambda r: r[2]) if sort_key=="name" else (lambda r: r[0]))
    return sorted(rows, key=keyfn, reverse=not asc)

async def send_md(update_or_query, text: str):
    MAX = 3800
    parts, buf = [], ""
    for line in text.splitlines(True):
        if len(buf)+len(line) > MAX:
            parts.append(buf)
            buf = ""
        buf += line
    if buf:
        parts.append(buf)
    for chunk in parts:
        if not chunk.startswith("```"):
            chunk = "```\n"+chunk
        if not chunk.rstrip().endswith("```"):
            chunk = chunk.rstrip()+"\n```"
        if hasattr(update_or_query, "message") and update_or_query.message:
            await update_or_query.message.reply_text(chunk, parse_mode="Markdown")
        else:
            await update_or_query.edit_message_text(chunk, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "lang" not in context.user_data:
        await update.message.reply_text(tr(context, "choose_lang"), reply_markup=lang_kb(context))
    elif "source" not in context.user_data:
        await update.message.reply_text(tr(context, "choose_source"), reply_markup=source_kb(context))
    elif "base" not in context.user_data:
        await update.message.reply_text(tr(context, "choose_base"), reply_markup=paged_codes_kb(context, "base", 0))
    else:
        await update.message.reply_text(tr(context, "main_menu"), reply_markup=main_menu_kb(context))

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(tr(context, "unknown"), reply_markup=main_menu_kb(context))

async def on_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data.startswith("lang:"):
        set_lang(context, data.split(":")[1])
        await q.edit_message_text(tr(context, "choose_source"), reply_markup=source_kb(context))
        return
    if data.startswith("src:"):
        set_source(context, data.split(":")[1])
        await q.edit_message_text(tr(context, "choose_base"), reply_markup=paged_codes_kb(context, "base", 0))
        return
    if data.startswith("base:page:"):
        page = int(data.split(":")[2])
        await q.edit_message_text(tr(context, "choose_base"), reply_markup=paged_codes_kb(context, "base", page))
        return
    if data.startswith("base:pick:"):
        base = data.split(":")[2]
        set_base(context, base)
        await q.edit_message_text(tr(context, "main_menu"), reply_markup=main_menu_kb(context))
        return
    if data == "menu:settings":
        await q.edit_message_text(tr(context, "settings_title"), reply_markup=settings_kb(context))
        return
    if data == "menu:main":
        await q.edit_message_text(tr(context, "main_menu"), reply_markup=main_menu_kb(context))
        return
    if data == "settings:lang":
        await q.edit_message_text(tr(context, "choose_lang"), reply_markup=lang_kb(context))
        return
    if data == "settings:source":
        await q.edit_message_text(tr(context, "choose_source"), reply_markup=source_kb(context))
        return
    if data == "settings:base":
        await q.edit_message_text(tr(context, "choose_base"), reply_markup=paged_codes_kb(context, "base", 0))
        return
    if data == "act:all":
        await show_all_rates(q, context, sort_key="code", asc=True)
        return
    if data == "act:convert":
        await q.edit_message_text(tr(context, "pick_target"), reply_markup=paged_codes_kb(context, "target", 0))
        return
    if data.startswith("target:page:"):
        page = int(data.split(":")[2])
        await q.edit_message_text(tr(context, "pick_target"), reply_markup=paged_codes_kb(context, "target", page))
        return
    if data.startswith("target:pick:"):
        context.user_data["target"] = data.split(":")[2]
        context.user_data["calc_input"] = ""
        await q.edit_message_text(tr(context, "enter_amount"), reply_markup=numpad_kb(context))
        return
    if data.startswith("sort:"):
        _, key, order = data.split(":")
        await show_all_rates(q, context, sort_key=key, asc=(order=="asc"))
        return
    if data.startswith("pad:"):
        cmd = data.split(":")[1]
        buf = context.user_data.get("calc_input", "")
        if cmd == "ok":
            await finalize_conversion(q, context)
            return
        if cmd == "clear":
            buf = ""
        elif cmd == "del":
            buf = buf[:-1]
        else:
            if not (cmd == "." and "." in buf):
                buf += cmd
        context.user_data["calc_input"] = buf
        await q.edit_message_text(f"{tr(context,'enter_amount')}\n`{buf or '0'}`", parse_mode="Markdown", reply_markup=numpad_kb(context))
        return

def get_rows_for_current(context: ContextTypes.DEFAULT_TYPE) -> List[Tuple[float,str,str]]:
    base = get_base(context)
    src = get_source(context)
    return api_table_for_base(base) if src == "api" else cbr_table_for_base(base)

async def show_all_rates(q, context, sort_key: str, asc: bool):
    rows = sort_rows(get_rows_for_current(context), sort_key, asc)
    base = get_base(context)
    header = tr(context, "rates_for", base=base)
    table = format_table(rows, header)
    try:
        await q.edit_message_text(table, parse_mode="Markdown", reply_markup=sorting_kb(context))
    except Exception:
        await send_md(q, table)
        await q.message.reply_text(tr(context, "sorting"), reply_markup=sorting_kb(context))

async def finalize_conversion(q, context):
    base = get_base(context)
    target = context.user_data.get("target")
    amount_str = context.user_data.get("calc_input") or "0"
    try:
        amt = float(amount_str)
    except ValueError:
        amt = 0.0
    rows = get_rows_for_current(context)
    rate_map: Dict[str, float] = {code: val for (val, code, _name) in rows}
    rate = rate_map.get(target)
    if rate is None:
        await q.edit_message_text(tr(context, "unknown"), reply_markup=main_menu_kb(context))
        return
    res = amt * rate
    msg = tr(context, "calc_result", amt=amt, base=base, res=f"{res:.6f}", target=target)
    await q.edit_message_text(f"```\n{msg}\n```", parse_mode="Markdown", reply_markup=main_menu_kb(context))

def main():
    persistence = PicklePersistence(filepath="bot_state.pickle")
    app = ApplicationBuilder().token(BOT_TOKEN).persistence(persistence).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.run_polling()

if __name__ == "__main__":
    main()