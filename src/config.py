import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CURRENCYLAYER_API_KEY = os.getenv("CURRENCYLAYER_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
if not CURRENCYLAYER_API_KEY:
    raise RuntimeError("CURRENCYLAYER_API_KEY is not set")