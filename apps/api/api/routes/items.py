"""HTTP surface for items.

Routes stay thin on purpose: validate the request shape, call the service,
return the result. No business rules, no try/except — domain errors are
translated centrally in ``api/error_handlers.py``.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from api.deps import get_items_service
from domain.items import Item, ItemStatus
from services.items import ItemsService

router = APIRouter(prefix="/items", tags=["items"])


class CreateItemRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class SetStatusRequest(BaseModel):
    status: ItemStatus


@router.get("/", response_model=list[Item])
def list_items(service: ItemsService = Depends(get_items_service)) -> list[Item]:
    return service.list_all()


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    body: CreateItemRequest, service: ItemsService = Depends(get_items_service)
) -> Item:
    return service.create(body.name)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: str, service: ItemsService = Depends(get_items_service)) -> Item:
    return service.get(item_id)


@router.patch("/{item_id}/status", response_model=Item)
def set_item_status(
    item_id: str,
    body: SetStatusRequest,
    service: ItemsService = Depends(get_items_service),
) -> Item:
    return service.set_status(item_id, body.status)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str, service: ItemsService = Depends(get_items_service)) -> None:
    service.delete(item_id)
