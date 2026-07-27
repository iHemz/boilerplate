"""Shared fixtures.

Every test gets an app whose repositories are fresh, so no test can depend on
state another test left behind. Nothing here reaches the network — a test that
hits the real Claude API or a real database is a bug, not a feature.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.deps import get_items_repository
from core.providers import AnthropicProvider, XAIProvider
from main import app
from repositories.items import InMemoryItemsRepository


@pytest.fixture(autouse=True)
def block_real_providers(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail loudly if a test tries to build a real model-provider client.

    Autouse, so it protects tests added later that forget to stub the model. A
    suite that can silently start billing a live account when a function is
    renamed is a hazard worth two lines of prevention.
    """

    def forbidden(self):
        raise AssertionError(
            f"A test tried to open a real {self.name.value} client. Stub the "
            "model instead — the suite must never call a paid API."
        )

    monkeypatch.setattr(AnthropicProvider, "_get_client", forbidden)
    monkeypatch.setattr(XAIProvider, "_get_client", forbidden)


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
