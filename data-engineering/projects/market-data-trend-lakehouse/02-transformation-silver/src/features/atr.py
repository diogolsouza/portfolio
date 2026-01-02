from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def add_atr(df: DataFrame, w: Window, period: int = 14) -> DataFrame:
    """Add ATR(period) using True Range and a simple moving average over the lookback window."""
    prev_close = F.lag("close", 1).over(w)
    tr = F.greatest(
        F.col("high") - F.col("low"),
        F.abs(F.col("high") - prev_close),
        F.abs(F.col("low") - prev_close),
    )
    out = df.withColumn("__tr", tr)
    w_atr = w.rowsBetween(-period + 1, 0)
    out = out.withColumn(f"atr_{period}", F.avg(F.col("__tr")).over(w_atr)).drop("__tr")
    return out
