from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def add_rules_v1_trend(
    df: DataFrame,
    ema_fast_col: str,
    ema_slow_col: str,
    atr_col: str,
    s_min: float,
    out_trend_col: str = "trend",
    out_strength_col: str = "trend_strength",
) -> DataFrame:
    """Rules-based baseline trend (v1). Deterministic and auditable.

    UP:
      ema_fast > ema_slow AND (ema_fast - ema_slow)/atr >= S_min

    DOWN:
      ema_fast < ema_slow AND (ema_fast - ema_slow)/atr <= -S_min

    Else: FLAT

    trend_strength = abs((ema_fast - ema_slow)/atr)
    """
    eps = F.lit(1e-9)
    diff = F.col(ema_fast_col) - F.col(ema_slow_col)
    s = diff / F.greatest(F.col(atr_col), eps)

    trend = (
        F.when((F.col(ema_fast_col) > F.col(ema_slow_col)) & (s >= F.lit(s_min)), F.lit("UP"))
         .when((F.col(ema_fast_col) < F.col(ema_slow_col)) & (s <= F.lit(-s_min)), F.lit("DOWN"))
         .otherwise(F.lit("FLAT"))
    )
    strength = F.abs(s)

    return df.withColumn(out_trend_col, trend).withColumn(out_strength_col, strength)
