from __future__ import annotations

from typing import Any, Dict

from .base import MarketDataProvider
from .example_stub import ExampleStubProvider


def build_provider(source: str, source_options: Dict[str, Any]) -> MarketDataProvider:
    """
    Factory for providers. Add real providers here as you implement them.

    source_options should include any credentials or endpoints (prefer Key Vault-backed secrets).
    """
    source = (source or "").strip().lower()

    if source in {"example_stub", "stub", "demo"}:
        return ExampleStubProvider(source_options)

    # TODO: Add real providers here:
    # if source == "alpha_vantage":
    #     return AlphaVantageProvider(source_options)
    # if source == "polygon":
    #     return PolygonProvider(source_options)
    # if source == "binance":
    #     return BinanceProvider(source_options)

    raise ValueError(f"Unknown provider source='{source}'. Implement it in build_provider().")
