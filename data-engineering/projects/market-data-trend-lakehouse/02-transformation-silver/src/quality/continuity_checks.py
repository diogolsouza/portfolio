from __future__ import annotations

from typing import Dict

INTERVAL_SECONDS: Dict[str, int] = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "4h": 14400,
    "1d": 86400
}


def interval_to_seconds(interval: str) -> int:
    i = (interval or "").strip().lower()
    if i not in INTERVAL_SECONDS:
        raise ValueError(f"Unsupported interval '{interval}'. Add it to INTERVAL_SECONDS.")
    return INTERVAL_SECONDS[i]
