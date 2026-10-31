"""Backward-compatible imports for the dashboard HTTP server."""

from traceforge.api.app import factory, serve

__all__ = ["factory", "serve"]
