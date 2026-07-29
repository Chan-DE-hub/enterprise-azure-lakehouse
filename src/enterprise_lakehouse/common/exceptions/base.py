"""Base exception hierarchy for the enterprise lakehouse platform."""

from __future__ import annotations


class EnterpriseLakehouseError(Exception):
    """Base exception for all platform-specific errors."""
