from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def add_gap_flag(df: DataFrame, w: Window, expected_seconds: int, tolerance_multiplier: float = 1.05) -> DataFrame:
    """Flag gaps where delta(ts) exceeds expected interval (with tolerance)."""
    prev_ts = F.lag("ts_utc", 1).over(w)
    delta_sec = (F.col("ts_utc").cast("long") - prev_ts.cast("long"))
    threshold = int(expected_seconds * tolerance_multiplier)

    return (
        df
        .withColumn("__prev_ts", prev_ts)
        .withColumn(
            "data_quality_flag",
            F.when(F.col("__prev_ts").isNull(), F.lit("OK"))
             .when(delta_sec > F.lit(threshold), F.lit("GAP"))
             .otherwise(F.lit("OK"))
        )
        .drop("__prev_ts")
    )
