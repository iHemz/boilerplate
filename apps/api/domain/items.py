"""Domain model and pure logic for items — the reference vertical slice.

This layer knows nothing about HTTP or storage. Everything here is a plain
value object or a pure function, which is why it needs no fixtures to test.
Replace this file with your real domain; keep the shape.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field


class ItemStatus(StrEnum):
    DRAFT = "draft"
    READY = "ready"
    ARCHIVED = "archived"


class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(min_length=1, max_length=200)
    status: ItemStatus = ItemStatus.DRAFT
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# Which transitions are legal. Encoding this as data rather than a chain of
# if-statements keeps the rule readable and makes it trivial to extend.
_ALLOWED_TRANSITIONS: dict[ItemStatus, frozenset[ItemStatus]] = {
    ItemStatus.DRAFT: frozenset({ItemStatus.READY, ItemStatus.ARCHIVED}),
    ItemStatus.READY: frozenset({ItemStatus.ARCHIVED}),
    ItemStatus.ARCHIVED: frozenset(),
}


def can_transition(current: ItemStatus, target: ItemStatus) -> bool:
    """Whether an item may move from ``current`` to ``target``."""
    return target in _ALLOWED_TRANSITIONS[current]
