from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def add_adx(df: DataFrame, w: Window, period: int = 14) -> DataFrame:
    """Add ADX(period) (optional) using a simplified, deterministic implementation."""
    up_move = F.col("high") - F.lag("high", 1).over(w)
    down_move = F.lag("low", 1).over(w) - F.col("low")

    plus_dm = F.when((up_move > down_move) & (up_move > 0), up_move).otherwise(F.lit(0.0))
    minus_dm = F.when((down_move > up_move) & (down_move > 0), down_move).otherwise(F.lit(0.0))

    prev_close = F.lag("close", 1).over(w)
    tr = F.greatest(
        F.col("high") - F.col("low"),
        F.abs(F.col("high") - prev_close),
        F.abs(F.col("low") - prev_close),
    )

    w_p = w.rowsBetween(-period + 1, 0)
    atr = F.avg(tr).over(w_p)

    plus_di = 100 * (F.avg(plus_dm).over(w_p) / atr)
    minus_di = 100 * (F.avg(minus_dm).over(w_p) / atr)

    dx = 100 * (F.abs(plus_di - minus_di) / (plus_di + minus_di))
    adx = F.avg(dx).over(w.rowsBetween(-period + 1, 0))

    return df.withColumn(f"adx_{period}", adx)
