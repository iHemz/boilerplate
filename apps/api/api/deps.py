"""The assembly layer — where concrete implementations meet the interfaces.

This is the only module that knows both which repository implementation is in
use and which service needs it. Routes depend on these providers; tests
override them with fakes via ``app.dependency_overrides``.
"""

from __future__ import annotations

from functools import lru_cache

from repositories.items import InMemoryItemsRepository, ItemsRepository
from services.items import ItemsService


@lru_cache
def get_items_repository() -> ItemsRepository:
    """One repository instance for the process.

    Cached because the in-memory implementation *is* the storage — a fresh
    instance per request would lose every write. A database-backed repository
    would drop the cache and take a session/connection argument instead.
    """
    return InMemoryItemsRepository()


def get_items_service() -> ItemsService:
    return ItemsService(get_items_repository())
