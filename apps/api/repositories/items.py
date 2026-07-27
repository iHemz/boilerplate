"""Data access for items — the only layer that touches storage.

The protocol is what services depend on; the in-memory class is one
implementation of it. Swapping in Postgres means writing a second class that
satisfies the same protocol and changing one line in ``api/deps.py`` — no
service, domain, or route code moves.
"""

from __future__ import annotations

from typing import Protocol

from domain.items import Item


class ItemsRepository(Protocol):
    """The storage contract. Services depend on this, never on a concrete class."""

    def add(self, item: Item) -> Item: ...

    def get(self, item_id: str) -> Item | None: ...

    def list_all(self) -> list[Item]: ...

    def save(self, item: Item) -> Item: ...

    def delete(self, item_id: str) -> bool: ...


class InMemoryItemsRepository:
    """Process-local storage. Correct for a demo, wrong for production.

    State lives on the instance rather than in a module-level dict so tests get
    a clean repository per case without teardown. The provider in ``api/deps.py``
    holds one long-lived instance for the app.
    """

    def __init__(self) -> None:
        self._items: dict[str, Item] = {}

    def add(self, item: Item) -> Item:
        self._items[item.id] = item
        return item

    def get(self, item_id: str) -> Item | None:
        return self._items.get(item_id)

    def list_all(self) -> list[Item]:
        return sorted(self._items.values(), key=lambda i: i.created_at)

    def save(self, item: Item) -> Item:
        self._items[item.id] = item
        return item

    def delete(self, item_id: str) -> bool:
        return self._items.pop(item_id, None) is not None
