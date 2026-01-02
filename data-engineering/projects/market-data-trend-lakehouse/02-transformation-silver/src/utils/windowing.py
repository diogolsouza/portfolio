from __future__ import annotations

from pyspark.sql import Window


def w_partition(symbol_col: str = "symbol", interval_col: str = "bar_interval", order_col: str = "ts_utc") -> Window:
    """Canonical window for per-symbol/per-interval time-ordered computations."""
    return Window.partitionBy(symbol_col, interval_col).orderBy(order_col)
