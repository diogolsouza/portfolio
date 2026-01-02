from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class BarRecord:
    """
    Canonical bar record for Bronze ingestion.

    Notes:
    - event_time_utc must represent the bar close time in UTC.
    - source_payload can store raw JSON/text if full fidelity is required.
    """
    event_time_utc: datetime
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None

    source_event_time: Optional[datetime] = None
    source_payload: Optional[str] = None
    source_batch_id: Optional[str] = None
    record_hash: Optional[str] = None


class MarketDataProvider(ABC):
    """
    Provider interface to decouple ingestion pipelines from specific APIs.

    Implementations must return normalized BarRecord objects.
    """

    @abstractmethod
    def fetch_bars(
        self,
        asset_class: str,
        symbol: str,
        interval: str,
        mode: str,
        as_of_utc: Optional[str],
    ) -> List[BarRecord]:
        """
        Fetch bars for a symbol and interval.

        mode:
          - "incremental": fetch latest bars since last watermark (provider-specific approach)
          - "backfill": fetch historical range (provider-specific approach)

        as_of_utc:
          Optional override timestamp for deterministic runs.
        """
        raise NotImplementedError

    @abstractmethod
    def name(self) -> str:
        """Short provider identifier (e.g., 'alpha_vantage', 'polygon', 'binance')."""
        raise NotImplementedError
