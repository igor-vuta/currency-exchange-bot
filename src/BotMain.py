# src/BotMain.py
import os
import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from config import BOT_TOKEN
from WEBScrappa import (
    get_exchange_rates, sort_by_code_webscraping,
    sort_by_definition_webscraping, sort_by_rate_webscraping
)
from APIRate import (
    main_api_rows,
    sort_by_rate_api, sort_by_currency_code_api, sort_by_currency_name_api
)

# ---- i18n ----
MESSAGES = {
    "en": {
        "greet": "Hello! How should I address you?",
        "source_prompt": "Nice to meet you, {name}. What would you like to use?",
        "menu_web": "Exchange rates – web scraping (CBR)",
        "menu_api": "Exchange rates – API (Currencylayer)",
        "sorting_prompt": "Which sorting do you want to apply?",
        "unknown": "Sorry, I didn’t understand. Please choose one of the options.",
        "date_rates": "Exchange rates for {date}:",
        "sort_web_name_asc": "Sort ↑ by name",
        "sort_web_name_desc": "Sort ↓ by name",
        "sort_web_code_asc": "Sort ↑ by code",
        "sort_web_code_desc": "Sort ↓ by code",
        "sort_web_rate_asc": "Sort ↑ by purchasing power",
        "sort_web_rate_desc": "Sort ↓ by purchasing power",
        "sort_api_code_asc": "Sort ↑ by currency code",
        "sort_api_code_desc": "Sort ↓ by currency code",
        "sort_api_name_asc": "Sort ↑ by currency name",
        "sort_api_name_desc": "Sort ↓ by currency name",
        "sort_api_rate_asc": "Sort ↑ by rate",
        "sort_api_rate_desc": "Sort ↓ by rate",
        "lang_switched": "Language switched to English.",
        "lang_help": "Use /lang ru or /lang en to switch language."
    },
    "ru": {
        "greet": "Здравствуйте, как к вам обращаться?",
        "source_prompt": "Рад знакомству, {name}. Какой вариант выберете?",
        "menu_web": "Курсы валют — web-scraping ЦБ",
        "menu_api": "Курсы валют — API (Currencylayer)",
        "sorting_prompt": "Какую сортировку хотите применить?",
        "unknown": "Извините, не понял запрос. Пожалуйста, выберите один из вариантов.",
        "date_rates": "Курсы валют на {date}:",
        "sort_web_name_asc": "Сортировка ↑ по названию",
        "sort_web_name_desc": "Сортировка ↓ по названию",
        "sort_web_code_asc": "Сортировка ↑ по коду",
        "sort_web_code_desc": "Сортировка ↓ по коду",
        "sort_web_rate_asc": "Сортировка ↑ по покупательной способности",
        "sort_web_rate_desc": "Сортировка ↓ по покупательной способности",
        "sort_api_code_asc": "Сортировка ↑ по коду валюты",
        "sort_api_code_desc": "Сортировка ↓ по коду валюты",
        "sort_api_name_asc": "Сортировка ↑ по названию валюты",
        "sort_api_name_desc": "Сортировка ↓ по названию валюты",
        "sort_api_rate_asc": "Сортировка ↑ по курсу",
        "sort_api_rate_desc": "Сортировка ↓ по курсу",
        "lang_switched": "Язык переключен на русский.",
        "lang_help": "Используйте /lang ru или /lang en для смены языка."
    }
}

USER_LANG = {}

def tr(user_id: int, key: str) -> str:
    lang = USER_LANG.get(user_id, "ru")
    return MESSAGES[lang][key]

USER_NAME_STATE = 1
EXCHANGE_RATE_STATE = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    USER_LANG[update.effective_user.id] = USER_LANG.get(update.effective_user.id, "ru")
    await update.message.reply_text(tr(update.effective_user.id, "greet"))
    context.user_data["state"] = USER_NAME_STATE

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args and context.args[0].lower() in ("ru", "en"):
        USER_LANG[update.effective_user.id] = context.args[0].lower()
        await update.message.reply_text(tr(update.effective_user.id, "lang_switched"))
    else:
        await update.message.reply_text(tr(update.effective_user.id, "lang_help"))

async def send_long_message(update, message):
    for i in range(0, len(message), 4096):
        await update.message.reply_text(message[i:i+4096])

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("state") == USER_NAME_STATE:
        user_id = update.effective_user.id
        user_name = update.message.text
        context.user_data["name"] = user_name
        markup = ReplyKeyboardMarkup(
            [[tr(user_id, "menu_web"), tr(user_id, "menu_api")]],
            one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            tr(user_id, "source_prompt").format(name=user_name),
            reply_markup=markup
        )
        context.user_data["state"] = EXCHANGE_RATE_STATE

async def get_rate_from_site(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    rate = sort_by_code_webscraping(get_exchange_rates(), ascending=True)
    await update.message.reply_text(f"{tr(user_id, 'date_rates').format(date=datetime.date.today())}\n{rate}")

    markup = ReplyKeyboardMarkup(
        [[tr(user_id,"sort_web_name_asc"), tr(user_id,"sort_web_name_desc")],
         [tr(user_id,"sort_web_code_asc"), tr(user_id,"sort_web_code_desc")],
         [tr(user_id,"sort_web_rate_asc"), tr(user_id,"sort_web_rate_desc")]],
        one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(tr(user_id, "sorting_prompt"), reply_markup=markup)
    context.user_data["state"] = "webscraping_sort"

async def get_rate_from_api(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    rows = main_api_rows()
    await send_long_message(update, sort_by_rate_api(rows, reverse=True))

    markup = ReplyKeyboardMarkup(
        [[tr(user_id,"sort_api_code_asc"), tr(user_id,"sort_api_code_desc")],
         [tr(user_id,"sort_api_name_asc"), tr(user_id,"sort_api_name_desc")],
         [tr(user_id,"sort_api_rate_asc"), tr(user_id,"sort_api_rate_desc")]],
        one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(tr(user_id, "sorting_prompt"), reply_markup=markup)
    context.user_data["state"] = "api_sort"

async def handle_rate_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    state = context.user_data.get("state")

    if state == USER_NAME_STATE:
        await handle_name(update, context)

    elif state == EXCHANGE_RATE_STATE:
        if update.message.text == tr(user_id, "menu_web"):
            await get_rate_from_site(update, context)
        elif update.message.text == tr(user_id, "menu_api"):
            await get_rate_from_api(update, context)
        else:
            await default_response(update, context)

    elif state == "webscraping_sort":
        txt = update.message.text
        if txt == tr(user_id,"sort_web_name_asc"):
            await send_long_message(update, sort_by_definition_webscraping(get_exchange_rates(), ascending=True))
        elif txt == tr(user_id,"sort_web_name_desc"):
            await send_long_message(update, sort_by_definition_webscraping(get_exchange_rates(), ascending=False))
        elif txt == tr(user_id,"sort_web_code_asc"):
            await send_long_message(update, sort_by_code_webscraping(get_exchange_rates(), ascending=True))
        elif txt == tr(user_id,"sort_web_code_desc"):
            await send_long_message(update, sort_by_code_webscraping(get_exchange_rates(), ascending=False))
        elif txt == tr(user_id,"sort_web_rate_asc"):
            await send_long_message(update, sort_by_rate_webscraping(get_exchange_rates(), ascending=True))
        elif txt == tr(user_id,"sort_web_rate_desc"):
            await send_long_message(update, sort_by_rate_webscraping(get_exchange_rates(), ascending=False))

    elif state == "api_sort":
        txt = update.message.text
        rows = main_api_rows()
        if txt == tr(user_id,"sort_api_code_asc"):
            await send_long_message(update, sort_by_currency_code_api(rows, reverse=False))
        elif txt == tr(user_id,"sort_api_code_desc"):
            await send_long_message(update, sort_by_currency_code_api(rows, reverse=True))
        elif txt == tr(user_id,"sort_api_name_asc"):
            await send_long_message(update, sort_by_currency_name_api(rows, reverse=False))
        elif txt == tr(user_id,"sort_api_name_desc"):
            await send_long_message(update, sort_by_currency_name_api(rows, reverse=True))
        elif txt == tr(user_id,"sort_api_rate_asc"):
            await send_long_message(update, sort_by_rate_api(rows, reverse=False))
        elif txt == tr(user_id,"sort_api_rate_desc"):
            await send_long_message(update, sort_by_rate_api(rows, reverse=True))
    else:
        await default_response(update, context)

async def default_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    markup = ReplyKeyboardMarkup(
        [[tr(user_id, "menu_web"), tr(user_id, "menu_api")]],
        one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(tr(user_id, "unknown"), reply_markup=markup)
    context.user_data["state"] = EXCHANGE_RATE_STATE

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lang", set_lang)) 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_rate_selection))
    app.run_polling()

if __name__ == "__main__":
    main()