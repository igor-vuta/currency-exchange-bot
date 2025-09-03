## 🤖 Exchange Rate Bot (Telegram)

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/python--telegram--bot-21.x-2CA5E0?logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/HTTP-httpx/requests-000000" />
  <img src="https://img.shields.io/badge/HTML-BeautifulSoup4-1f6feb" />
  <img src="https://img.shields.io/badge/Deployment-Heroku-purple" />
</div>



---

## A production‑ready Telegram bot that provides real‑time currency exchange rates from two sources:
	-	🌐 Currencylayer API (live market quotes)
	-	🏦 Central Bank of Russia (official daily rates via web‑scraping)

Users can browse, sort, and search rates with a friendly chat flow and Telegram keyboards.

Try the bot: @ExchangeRateBotProviderBot (update in this README if your handle changes)

---

## ✨ Features
	-	⚡ Live rates via Currencylayer
	-	🏦 Official CBR rates via BeautifulSoup scraping
	-	🔎 Sorting & filtering: by rate, currency code, or currency name
	-	🧭 Guided UX with Telegram reply/inline keyboards
	-	🌍 Multi‑language ready (current prompts in Russian)
	-	🧪 Simple to run locally; Heroku‑friendly (Procfile & runtime.txt included)

---

## 🗂 Project Structure

currencyExchange/
├── .env.example           # Example of required environment variables (do NOT commit real secrets)
├── Procfile               # Heroku entrypoint
├── README.md              # You are here
├── requirements.txt       # Python dependencies
├── runtime.txt            # Heroku Python runtime
└── src/
    ├── APIRate.py         # Currencylayer fetching & currency metadata
    ├── WEBScrappa.py      # Central Bank scraper (BeautifulSoup)
    └── BotMain.py         # Telegram bot flow & handlers


---

## ⚙️ Tech Stack

Area	Tools
Bot	python-telegram-bot 21.x
HTTP	requests, httpx
Scraping	BeautifulSoup4
Runtime	Python 3.11+
Deploy	Heroku (Procfile), or any VM/Container


---

## 🚀 Quick Start (Local)
	1.	Clone & enter the project

git clone <your-new-repo-url> currency-exchange-bot
cd currency-exchange-bot

	2.	Create & activate venv (recommended)

python3 -m venv .venv
source ./.venv/bin/activate   # Windows: .\.venv\Scripts\activate

	3.	Install dependencies

pip install -r requirements.txt

	4.	Configure environment
Create a .env file (copy from .env.example) and set:

BOT_TOKEN=your_telegram_bot_token
CURRENCYLAYER_API_KEY=your_currencylayer_key

## 🔐 Security tip: The repo you uploaded had hard‑coded keys. Move all secrets into .env and rotate any exposed tokens.

	5.	Run the bot

python src/BotMain.py


---

## ☁️ Deploy (Heroku)

Heroku files are already present. Minimal flow:

# Create app
heroku create your-bot-name

# Set environment variables
heroku config:set BOT_TOKEN=... CURRENCYLAYER_API_KEY=...

# Push code
git push heroku main

# View logs
heroku logs --tail

Alternative: run on Render, Railway, Fly.io, or a Dockerized VPS. The entrypoint is python src/BotMain.py.

---

## 🧭 Bot Commands & UX
	-	/start — greet user & show main menu
	-	Get exchange rates — choose between Currencylayer live rates or CBR official daily rates
	-	Sorting — sort by currency code/name or by numeric rate
	-	Navigation — reply keyboards guide users back/forth safely

Current prompts are in Russian. You can translate messages in BotMain.py to support EN/RU.

---

## 🔌 Integrations

Currencylayer
	-	Endpoint: http://api.currencylayer.com/live
	-	Auth: access_key param
	-	Notes: Free tier updates hourly; HTTPS on paid tiers. Respect API limits.

Central Bank of Russia (CBR)
	-	Scraped HTML table via BeautifulSoup.
	-	Be mindful of structure changes; handle missing/renamed columns gracefully.

---

## 🧱 Architecture (high‑level)

[User]
  ⬇︎ Telegram
[python-telegram-bot]
  ⬇︎ handlers
[BotMain.py] ── calls ──> [APIRate.py]  (Currencylayer)
                 └──────> [WEBScrappa.py] (CBR scraper)

	-	BotMain.py manages state & conversation flow using ApplicationBuilder.
	-	APIRate.py fetches live quotes & holds a currency code → human name mapping.
	-	WEBScrappa.py scrapes the CBR table and normalizes rates.

---

## 🧹 Code Quality & Hardening Checklist
	-	Move API keys to .env (BOT_TOKEN, CURRENCYLAYER_API_KEY)
	-	Use HTTPS for Currencylayer if your plan allows
	-	Add retries/timeouts to HTTP requests (httpx/requests)
	-	Validate API responses & handle rate‑limits
	-	Exception logging around network/scraping calls
	-	Dockerfile (optional) for reproducible deploys

---

## 🖼 Screenshots

Add real Telegram chat screenshots here (PNG/JPEG):

/docs/screenshots/
  01-start.png
  02-source-selection.png
  03-cbr-rates.png
  04-currencylayer-rates.png
  05-sorting.png

Sample Markdown in this README:

![Start](docs/screenshots/01-start.png)
![Source selection](docs/screenshots/02-source-selection.png)


---

## 🔐 Environment Variables

Name	Required	Example
BOT_TOKEN	✅	123456:ABCDEF...
CURRENCYLAYER_API_KEY	✅	abcd1234...

Remove any hard‑coded keys from APIRate.py and replace with os.getenv("CURRENCYLAYER_API_KEY").

---

## 📦 Requirements

From requirements.txt (pinned): python-telegram-bot, requests, httpx, beautifulsoup4, etc. Use:

pip install -r requirements.txt


---

## 📜 License

Choose a license (e.g., MIT) and add a LICENSE file. Example badge:

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)


---

🏁 Repush Plan (Option A: squash)

# from a fresh working copy of the project
rm -rf .git
git init
git add .
git commit -S -m "chore: initial import"
git branch -M main
git remote add origin git@github.com:<new-user>/<new-repo>.git
git push -u origin main

After pushing: upload screenshots, update this README with your actual bot handle, and rotate any tokens that were ever committed.