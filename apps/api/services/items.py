"""Use-cases for items — orchestration between routes and storage.

Services own the "what should happen" decisions and raise domain errors when
the answer is no. They never import FastAPI, so the same service is callable
from a route, a CLI, a worker, or a test with equal ease.
"""

from __future__ import annotations

from core.errors import BadRequestError, NotFoundError
from domain.items import Item, ItemStatus, can_transition
from repositories.items import ItemsRepository


class ItemsService:
    def __init__(self, repository: ItemsRepository) -> None:
        self._repository = repository

    def create(self, name: str) -> Item:
        return self._repository.add(Item(name=name))

    def get(self, item_id: str) -> Item:
        item = self._repository.get(item_id)
        if item is None:
            raise NotFoundError(f"No item with id {item_id!r}.")
        return item

    def list_all(self) -> list[Item]:
        return self._repository.list_all()

    def set_status(self, item_id: str, status: ItemStatus) -> Item:
        item = self.get(item_id)
        if item.status == status:
            return item
        if not can_transition(item.status, status):
            raise BadRequestError(f"Cannot move an item from {item.status} to {status}.")
        return self._repository.save(item.model_copy(update={"status": status}))

    def delete(self, item_id: str) -> None:
        if not self._repository.delete(item_id):
            raise NotFoundError(f"No item with id {item_id!r}.")
