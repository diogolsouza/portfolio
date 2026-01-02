from __future__ import annotations

from typing import Iterable

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def add_log_returns(df: DataFrame, w: Window, lags: Iterable[int], price_col: str = "close") -> DataFrame:
    """Add log returns for the provided lags. Deterministic and strategy-agnostic."""
    out = df
    for k in lags:
        out = out.withColumn(f"return_{k}", F.log(F.col(price_col) / F.lag(price_col, k).over(w)))
    return out
