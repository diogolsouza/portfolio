from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def add_rules_confidence(
    df: DataFrame,
    strength_col: str,
    s_min: float,
    scale_mult: float = 2.0,
    cap_at: float = 1.0,
    out_col: str = "confidence",
) -> DataFrame:
    """Rule-based confidence proxy when ML is not present."""
    denom = F.lit(max(s_min * scale_mult, 1e-9))
    conf = F.least(F.col(strength_col) / denom, F.lit(cap_at))
    return df.withColumn(out_col, conf)
