"""Redis-backed persistence for the Telegram bot."""

import json
import logging
import os
from copy import deepcopy
from typing import Any, Dict, Optional, Tuple, Union

import redis
from telegram.ext import BasePersistence, PersistenceInput

logger = logging.getLogger(__name__)

UD = Any
CD = Any
BD = Any
ConversationDict = Dict[Tuple[Union[int, str], ...], object]


class RedisPersistence(BasePersistence[UD, CD, BD]):
    """Stores bot/user/chat data in Redis so state survives container restarts.

    Args:
        url: Redis connection URL. Falls back to ``REDIS_URL`` env var,
            then ``redis://localhost:6379/0``.
        key_prefix: Prefix for all Redis keys used by this bot.
        store_data: Which data kinds to persist. Defaults to user, chat, and bot data.
        update_interval: How often the application flushes pending updates.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        key_prefix: str = "currency_bot",
        store_data: Optional[PersistenceInput] = None,
        update_interval: float = 60,
    ):
        super().__init__(store_data=store_data, update_interval=update_interval)
        self.url = url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.key_prefix = key_prefix
        self._redis: Optional[redis.Redis] = None

    @property
    def redis(self) -> redis.Redis:
        if self._redis is None:
            logger.info("Connecting to Redis at %s", self.url)
            self._redis = redis.from_url(self.url, decode_responses=True)
        return self._redis

    def _key(self, suffix: str) -> str:
        return f"{self.key_prefix}:{suffix}"

    def _get_json(self, key: str) -> Optional[Any]:
        try:
            raw = self.redis.get(key)
        except redis.RedisError as exc:
            logger.warning("Redis GET %s failed: %s", key, exc)
            return None
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.warning("Failed to decode Redis value for %s: %s", key, exc)
            return None

    def _set_json(self, key: str, value: Any) -> None:
        try:
            self.redis.set(key, json.dumps(value))
        except redis.RedisError as exc:
            logger.warning("Redis SET %s failed: %s", key, exc)

    async def get_bot_data(self) -> BD:
        if not self.store_data.bot_data:
            return {}
        data = self._get_json(self._key("bot_data"))
        return deepcopy(data) if data is not None else {}

    async def update_bot_data(self, data: BD) -> None:
        if self.store_data.bot_data:
            self._set_json(self._key("bot_data"), data)

    async def refresh_bot_data(self, data: BD) -> None:
        pass

    async def drop_bot_data(self) -> None:
        try:
            self.redis.delete(self._key("bot_data"))
        except redis.RedisError as exc:
            logger.warning("Redis DELETE bot_data failed: %s", exc)

    async def get_user_data(self) -> Dict[int, UD]:
        if not self.store_data.user_data:
            return {}
        data = self._get_json(self._key("user_data"))
        return {int(k): deepcopy(v) for k, v in (data or {}).items()}

    async def update_user_data(self, user_id: int, data: UD) -> None:
        if self.store_data.user_data:
            key = self._key("user_data")
            current = self._get_json(key) or {}
            current[str(user_id)] = data
            self._set_json(key, current)

    async def refresh_user_data(self, user_id: int, data: UD) -> None:
        pass

    async def drop_user_data(self, user_id: int) -> None:
        key = self._key("user_data")
        current = self._get_json(key) or {}
        current.pop(str(user_id), None)
        self._set_json(key, current)

    async def get_chat_data(self) -> Dict[int, CD]:
        if not self.store_data.chat_data:
            return {}
        data = self._get_json(self._key("chat_data"))
        return {int(k): deepcopy(v) for k, v in (data or {}).items()}

    async def update_chat_data(self, chat_id: int, data: CD) -> None:
        if self.store_data.chat_data:
            key = self._key("chat_data")
            current = self._get_json(key) or {}
            current[str(chat_id)] = data
            self._set_json(key, current)

    async def refresh_chat_data(self, chat_id: int, data: CD) -> None:
        pass

    async def drop_chat_data(self, chat_id: int) -> None:
        key = self._key("chat_data")
        current = self._get_json(key) or {}
        current.pop(str(chat_id), None)
        self._set_json(key, current)

    async def get_callback_data(self) -> Optional[Tuple[Any, ...]]:
        if not self.store_data.callback_data:
            return None
        data = self._get_json(self._key("callback_data"))
        return deepcopy(data) if data is not None else None

    async def update_callback_data(self, data: Tuple[Any, ...]) -> None:
        if self.store_data.callback_data:
            self._set_json(self._key("callback_data"), data)

    async def drop_callback_data(self) -> None:
        try:
            self.redis.delete(self._key("callback_data"))
        except redis.RedisError as exc:
            logger.warning("Redis DELETE callback_data failed: %s", exc)

    async def get_conversations(self, name: str) -> ConversationDict:
        if not self.store_data.conversations:
            return {}
        data = self._get_json(self._key(f"conversation:{name}"))
        return deepcopy(data) if data is not None else {}

    async def update_conversation(
        self,
        name: str,
        key: Tuple[Union[int, str], ...],
        new_state: Optional[object],
    ) -> None:
        if self.store_data.conversations:
            redis_key = self._key(f"conversation:{name}")
            current = self._get_json(redis_key) or {}
            current[str(key)] = new_state
            self._set_json(redis_key, current)

    async def flush(self) -> None:
        # Data is written immediately; nothing extra to flush.
        pass
