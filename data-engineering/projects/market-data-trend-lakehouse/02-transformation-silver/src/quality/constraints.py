from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def enforce_ohlc_sanity(df: DataFrame) -> DataFrame:
    """Overwrite data_quality_flag with INVALID_OHLC when OHLC constraints are violated."""
    invalid = (
        (F.col("high") < F.greatest(F.col("open"), F.col("close"))) |
        (F.col("low") > F.least(F.col("open"), F.col("close"))) |
        (F.col("high") < F.col("low"))
    )
    return df.withColumn(
        "data_quality_flag",
        F.when(invalid, F.lit("INVALID_OHLC")).otherwise(F.col("data_quality_flag"))
    )
