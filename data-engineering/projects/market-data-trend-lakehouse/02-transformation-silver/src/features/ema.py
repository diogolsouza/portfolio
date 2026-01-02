from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def add_ema(df: DataFrame, w: Window, period: int, price_col: str = "close", out_col: str = "ema") -> DataFrame:
    """Approximate EMA using exponentially decaying weights over a finite window.

    Spark does not provide a built-in EMA aggregate. For portfolio purposes, this uses a finite-window
    weighted average approximation that is deterministic and reproducible.

    For production trading systems, consider stateful streaming EMA or a Pandas UDF per group.
    """
    lookback = period * 5
    w_lb = w.rowsBetween(-lookback, 0)
    alpha = 2.0 / (period + 1.0)

    out = (
        df
        .withColumn("__price_arr", F.collect_list(F.col(price_col)).over(w_lb))
        .withColumn("__n", F.size(F.col("__price_arr")))
        .withColumn(
            "__weights",
            F.expr(f"transform(sequence(0, __n-1), i -> {alpha} * pow(1 - {alpha}, i))")
        )
        .withColumn("__weights_norm", F.expr("aggregate(__weights, 0D, (acc, x) -> acc + x)"))
        .withColumn(
            out_col,
            F.expr("aggregate(zip_with(__price_arr, __weights, (p, w) -> p*w), 0D, (acc, x) -> acc + x) / __weights_norm")
        )
        .drop("__price_arr", "__n", "__weights", "__weights_norm")
    )
    return out
