import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CURRENCYLAYER_API_KEY = os.getenv("CURRENCYLAYER_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def validate() -> None:
    """Validate required environment variables. Called at runtime, not import."""
    missing = []
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not CURRENCYLAYER_API_KEY:
        missing.append("CURRENCYLAYER_API_KEY")
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")