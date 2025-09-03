## 🤖 Currency Exchange Bot

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Telegram-bot-2CA5E0?logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/Scraping-BeautifulSoup4-1f6feb" />
  <img src="https://img.shields.io/badge/API-currencylayer-000000" />
  <img src="https://img.shields.io/badge/Deploy-Heroku%20|%20Railway%20|%20Render-purple" />
</div>

---

<p align="center">
  <a href="https://t.me/luxenonbeterris_exchange_bot" target="_blank">
    <img alt="Open on Telegram" src="https://img.shields.io/badge/Open%20on%20Telegram-@luxenonbeterris__exchange__bot-2CA5E0?logo=telegram&logoColor=white">
  </a>
</p>

---

## A clean, button‑only Telegram bot for currency rates and conversions. New users pick language → source → base currency, then choose between:
	-	1 BASE → all — view a well‑formatted table of rates for 1 base currency against all others (sortable).
	-	Convert amount — pick a target and enter an amount using an on‑screen numeric keypad (no typing).

Everything is persistent: language, data source (CBR/API), and base currency are saved and editable in Settings.

---

## ✨ Highlights
	-	🧭 Onboarding flow: Language → Source (CBR/API) → Base currency (paginated list)
	-	🧮 Calculator: keypad input, precise conversion, result in monospace
	-	📊 Tables: aligned monospace output with sorting (code/name/rate)
	-	💾 Persistence: user preferences survive bot restarts (PicklePersistence)
	-	🔐 Secure config: .env for BOT_TOKEN, CURRENCYLAYER_API_KEY
	-	🚀 Deployable anywhere: Heroku/Railway/Render or any VPS

---

## 🗂 Structure

src/
  APIRate.py     # currencylayer cross‑rates for arbitrary base
  BotMain.py     # button‑only flow, i18n, persistence, calculator
  WEBScrappa.py  # CBR rates via BeautifulSoup
  config.py      # loads secrets from .env
requirements.txt
Procfile | runtime.txt (optional for Heroku)


---

## ⚙️ Setup

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill values
python src/BotMain.py

.env

BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
CURRENCYLAYER_API_KEY=YOUR_CURRENCYLAYER_API_KEY


---

## 🧪 Try it
	1.	/start → choose language
	2.	Choose source: CBR or currencylayer
	3.	Choose base currency (paginated)
	4.	Main menu:
	-	1 BASE → all → view & sort table
	-	Convert amount → pick target → keypad → OK
	-	Settings → change language/source/base

---

## 🖼 Screenshots

Place images in docs/screenshots/ and reference here:

![Onboarding](docs/screenshots/01-onboarding.png)
![Table](docs/screenshots/02-table.png)
![Calculator](docs/screenshots/03-calculator.png)


---

## 🔐 Notes
	-	Rotate any previously exposed keys/tokens.
	-	Respect currencylayer free‑tier limitations.
	-	Scraper may require maintenance if CBR markup changes.

---

## 📜 License

[GNU Affero General Public License v3 (AGPLv3)](https://www.gnu.org/licenses/agpl-3.0.html)

- ✅ Share and showcase code freely.
- ✅ Others may learn and contribute.
- ❌ No one can take it private, build a SaaS on top, and profit without open-sourcing their changes.
