"""TTL caching for exchange-rate sources."""

import logging
import os
import time
from typing import Any, Optional

import redis

logger = logging.getLogger(__name__)

DEFAULT_TTL_SECONDS = int(os.getenv("RATE_CACHE_TTL", "300"))  # 5 minutes


class RateCache:
    """Simple TTL cache for exchange-rate data.

    Uses Redis when ``REDIS_URL`` is available, otherwise falls back to an
    in-memory dictionary.
    """

    def __init__(self, ttl_seconds: int = DEFAULT_TTL_SECONDS, url: Optional[str] = None):
        self.ttl = ttl_seconds
        self.url = url or os.getenv("REDIS_URL")
        self._memory: dict[str, tuple[float, Any]] = {}
        self._redis: Optional[redis.Redis] = None
        hosted = bool(
            os.getenv("PORT")
            or os.getenv("RAILWAY_ENVIRONMENT")
            or os.getenv("RAILWAY_SERVICE_NAME")
            or os.getenv("RENDER")
            or os.getenv("HEROKU_APP_ID")
        )
        if self.url and not (hosted and ("localhost" in self.url or "127.0.0.1" in self.url)):
            try:
                self._redis = redis.from_url(self.url, decode_responses=True)
                self._redis.ping()
                logger.info("Rate cache using Redis")
            except redis.RedisError as exc:
                logger.warning("Redis cache unavailable, using in-memory fallback: %s", exc)
                self._redis = None
        elif self.url and hosted:
            logger.warning(
                "REDIS_URL points to localhost in a hosted environment; "
                "using in-memory cache."
            )

    def _redis_key(self, key: str) -> str:
        return f"currency_bot:cache:{key}"

    def get(self, key: str) -> Optional[Any]:
        if self._redis is not None:
            try:
                raw = self._redis.get(self._redis_key(key))
                if raw is None:
                    return None
                import json

                return json.loads(raw)
            except redis.RedisError as exc:
                logger.warning("Redis cache read failed: %s", exc)
        else:
            expires_at, value = self._memory.get(key, (0, None))
            if time.monotonic() < expires_at:
                return value
        return None

    def set(self, key: str, value: Any) -> None:
        if self._redis is not None:
            try:
                import json

                self._redis.setex(self._redis_key(key), self.ttl, json.dumps(value))
            except redis.RedisError as exc:
                logger.warning("Redis cache write failed: %s", exc)
        else:
            self._memory[key] = (time.monotonic() + self.ttl, value)


# Module-level cache instance used by APIRate and WEBScrappa.
cache = RateCache()


def cached(key: str):
    """Decorator that caches a function's result under *key* for ``RateCache.ttl`` seconds."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = cache.get(key)
            if result is not None:
                logger.debug("Cache hit for %s", key)
                return result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result

        return wrapper

    return decorator
