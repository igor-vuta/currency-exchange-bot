<!-- project-presentation:start -->

![Currency Exchange Bot — Button-driven Telegram currency rates and conversions](.github/readme-header.svg)

**[Open bot](https://t.me/currenvy_bot_for_demo_bot)** · [Repository activity](https://github.com/igor-vuta/currency-exchange-bot/activity)

[![Last commit](https://img.shields.io/github/last-commit/igor-vuta/currency-exchange-bot?style=flat-square&color=6366f1)](https://github.com/igor-vuta/currency-exchange-bot/commits)
[![Repository size](https://img.shields.io/github/repo-size/igor-vuta/currency-exchange-bot?style=flat-square&color=6366f1)](https://github.com/igor-vuta/currency-exchange-bot)

**3** Interface languages · **2** Rate sources · **3** UI screenshots

*Project facts checked 2 October 2026. Activity badges update from GitHub.*

<!-- project-presentation:end -->

<div align="center">

# 🤖 Currency Exchange Bot

**A Telegram bot for currency rates and conversions, with button-driven setup and an inline calculator.**

<img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/python--telegram--bot-persistence-2CA5E0?logo=telegram&logoColor=white" />
<img src="https://img.shields.io/badge/Scraping-BeautifulSoup4-1f6feb" />
<img src="https://img.shields.io/badge/API-currencylayer-000000" />

<br />

### Open in Telegram

[![Open in Telegram](https://img.shields.io/badge/%F0%9F%9A%80%20Live%20demo-@currenvy__bot__for__demo__bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/currenvy_bot_for_demo_bot)

*The link opens the bot profile; availability and response time depend on the running bot and its rate providers.*

</div>

---

## What it does

New users walk through **language → data source → base currency**, then reach the rates and conversion actions:

- **1 BASE → all** — a clean, monospace-aligned table of your base currency against every other, sortable by code, name, or rate.
- **Convert amount** — pick a target currency and enter the amount on an inline numeric keypad.

```
┌──────────────────────────────┐
│  💱 1 USD → all              │
│                              │
│  EUR   European Euro   0.92  │
│  GBP   British Pound   0.78  │
│  KZT   Kazakh Tenge  478.11  │
│  RUB   Russian Ruble  87.45  │
│  ...                         │
│                              │
│  [Sort: rate ▾]  [⚙ Settings]│
└──────────────────────────────┘
```

Language, data source (CBR / currencylayer API), and base currency are editable in Settings. Configure Redis to keep user preferences across process restarts; without `REDIS_URL`, persistence is in memory only.

---

## ✨ Highlights

- 🧭 **Button-driven UX** — setup, sorting, settings, and conversion use inline buttons and a numeric keypad
- 🌍 **Multilingual** — English, Russian, and Chinese interfaces, switchable in Settings
- 🔀 **Dual data sources** — Central Bank of Russia (scraped with BeautifulSoup) or currencylayer API cross-rates, user's choice
- 📊 **Readable tables** — aligned monospace output with sorting (code / name / rate)
- 💾 **Optional Redis persistence** — user preferences survive restarts when `REDIS_URL` is configured; otherwise they remain in memory
- 🔐 **Secure config** — secrets in `.env` (`BOT_TOKEN`, `CURRENCYLAYER_API_KEY`), never in code
- 🚀 **Polling process with health endpoint** — `/health` listens on `PORT` (default `8080`); `Procfile` is included for compatible hosts

---

## 🗂 Structure

```
src/
  APIRate.py     # currencylayer cross-rates for an arbitrary base
  BotMain.py     # button-only flow, i18n, persistence, keypad calculator
  WEBScrappa.py  # CBR rates via BeautifulSoup
  config.py      # loads secrets from .env
  persistence.py # Redis or in-memory preference storage
requirements.txt
Procfile | runtime.txt   # optional, for Heroku-style deploys
```

---

## ⚙️ Run your own instance

```bash
uv venv
uv pip install -r requirements.txt
cp .env.example .env   # fill in your tokens
uv run --no-project python src/BotMain.py
```

`.env`:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
CURRENCYLAYER_API_KEY=YOUR_CURRENCYLAYER_API_KEY
# Optional: Redis for preferences that survive restarts
REDIS_URL=redis://localhost:6379/0
```

---

## 🧪 The flow

1. `/start` → choose English, Russian, or Chinese
2. Choose source: **CBR** or **currencylayer**
3. Choose base currency (paginated list)
4. Main menu:
   - **1 BASE → all** → view & sort the table
   - **Convert amount** → pick target → keypad → OK
   - **Settings** → change language / source / base at any time

---

## 🖼 Screenshots

<div align="center">
  <img src="docs/screenshots/01-onboarding.png" width="30%" alt="Onboarding — language, source, base currency" />
  <img src="docs/screenshots/02-table.png" width="30%" alt="Rates table — 1 BASE to all, sortable" />
  <img src="docs/screenshots/03-calculator.png" width="30%" alt="Keypad calculator — convert amount" />
</div>

---

## 🔐 Notes

- Rotate any previously exposed keys or tokens.
- Respect currencylayer free-tier limits.
- The CBR scraper may need maintenance if the bank's markup changes.

---

## 📜 License

[GNU Affero General Public License v3 (AGPLv3)](https://www.gnu.org/licenses/agpl-3.0.html)

- ✅ Share and showcase code freely.
- ✅ Others may learn and contribute under the license terms.
- 📖 Network service operators must make the corresponding source available to users as required by AGPLv3.

---

<div align="center">

Built by **[Igor Vuta](https://github.com/igor-vuta)** · [Portfolio](https://igor-vuta.github.io/portfolio/) · [LinkedIn](https://www.linkedin.com/in/igor-vuta-b88017390)

</div>
