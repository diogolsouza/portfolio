from __future__ import annotations

from typing import Optional


def normalize_symbol(symbol: str) -> str:
    """
    Normalize symbols across sources. Keep it simple and deterministic.
    Examples:
      - 'EURUSD' stays 'EURUSD'
      - 'BTC-USD' stays 'BTC-USD'
      - 'eurusd' -> 'EURUSD'
    """
    s = (symbol or "").strip()
    return s.upper()


def normalize_asset_class(asset_class: str) -> str:
    s = (asset_class or "").strip().upper()
    return s


def normalize_interval(interval: str) -> str:
    """
    Canonicalize interval strings (1m, 5m, 1h, 1d).
    """
    s = (interval or "").strip().lower()
    return s
