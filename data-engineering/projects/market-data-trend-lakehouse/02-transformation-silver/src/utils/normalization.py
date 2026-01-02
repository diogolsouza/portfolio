from __future__ import annotations


def normalize_symbol(symbol: str) -> str:
    return (symbol or "").strip().upper()


def normalize_asset_class(asset_class: str) -> str:
    return (asset_class or "").strip().upper()


def normalize_interval(interval: str) -> str:
    return (interval or "").strip().lower()
