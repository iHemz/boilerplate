"""Shared fixtures.

Every test gets an app whose repositories are fresh, so no test can depend on
state another test left behind. Nothing here reaches the network — a test that
hits the real Claude API or a real database is a bug, not a feature.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.deps import get_items_repository
from main import app
from repositories.items import InMemoryItemsRepository


@pytest.fixture
def items_repository() -> InMemoryItemsRepository:
    return InMemoryItemsRepository()


@pytest.fixture
def client(items_repository: InMemoryItemsRepository):
    app.dependency_overrides[get_items_repository] = lambda: items_repository
    # The service provider calls get_items_repository() directly rather than
    # through Depends, so clear its cache too — otherwise the override is
    # bypassed and tests share one repository.
    get_items_repository.cache_clear()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    get_items_repository.cache_clear()
