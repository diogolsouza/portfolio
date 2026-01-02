from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def add_volatility_state(
    df: DataFrame,
    w: Window,
    atr_col: str,
    window_bars: int = 288,
    low_mult: float = 0.8,
    high_mult: float = 1.2,
    out_col: str = "volatility_state",
) -> DataFrame:
    """Deterministic volatility state from ATR vs rolling ATR mean."""
    w_rb = w.rowsBetween(-window_bars + 1, 0)
    rolling_mean = F.avg(F.col(atr_col)).over(w_rb)

    return df.withColumn(
        out_col,
        F.when(F.col(atr_col) < rolling_mean * F.lit(low_mult), F.lit("LOW"))
         .when(F.col(atr_col) > rolling_mean * F.lit(high_mult), F.lit("HIGH"))
         .otherwise(F.lit("MED"))
    )
