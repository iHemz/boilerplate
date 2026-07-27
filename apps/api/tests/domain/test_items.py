"""Unit tests — pure domain logic, no fixtures, no I/O.

This is the cheapest and highest-value layer of the pyramid. Most new logic
should be testable here.
"""

from domain.items import ItemStatus, can_transition


def test_draft_can_become_ready():
    assert can_transition(ItemStatus.DRAFT, ItemStatus.READY)


def test_ready_cannot_go_back_to_draft():
    assert not can_transition(ItemStatus.READY, ItemStatus.DRAFT)


def test_archived_is_terminal():
    assert not can_transition(ItemStatus.ARCHIVED, ItemStatus.READY)
    assert not can_transition(ItemStatus.ARCHIVED, ItemStatus.DRAFT)
