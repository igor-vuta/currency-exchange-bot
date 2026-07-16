import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CURRENCYLAYER_API_KEY = os.getenv("CURRENCYLAYER_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
if not CURRENCYLAYER_API_KEY:
    raise RuntimeError("CURRENCYLAYER_API_KEY is not set")