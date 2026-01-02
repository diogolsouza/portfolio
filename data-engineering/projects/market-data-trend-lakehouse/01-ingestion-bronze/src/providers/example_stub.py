from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .base import BarRecord, MarketDataProvider


class ExampleStubProvider(MarketDataProvider):
    """
    Safe, zero-dependency provider used to validate the ingestion pipeline end-to-end.

    Returns an empty list by default (so scheduled jobs do not fail).
    You can optionally add deterministic fake bars for demos.
    """

    def __init__(self, source_options: Dict[str, Any]):
        self._opts = source_options or {}

    def name(self) -> str:
        return "example_stub"

    def fetch_bars(
        self,
        asset_class: str,
        symbol: str,
        interval: str,
        mode: str,
        as_of_utc: Optional[str],
    ) -> List[BarRecord]:
        # Default: return no data (safe for CI / workflow dry runs)
        if not self._opts.get("emit_sample_data", False):
            return []

        # Optional deterministic sample record (for demos/tests)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return [
            BarRecord(
                event_time_utc=now,
                open=1.0,
                high=1.1,
                low=0.9,
                close=1.05,
                volume=0.0,
                source_payload='{"sample": true}',
                source_batch_id="sample",
            )
        ]
