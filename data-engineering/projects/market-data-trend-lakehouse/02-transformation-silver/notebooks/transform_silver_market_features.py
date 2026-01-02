# Databricks notebook: 02-transformation-silver/notebooks/transform_silver_market_features.py
# Purpose: Build silver_market_features from silver_market_bars (EMA/ATR/Returns, optional ADX).

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict

from pyspark.sql import functions as F

# Parameters
dbutils.widgets.text("config_path", "dbfs:/FileStore/market-data/config/silver.json")
CONFIG_PATH = dbutils.widgets.get("config_path")

# Repo modules (update path)
REPO_ROOT = "/Workspace/Repos/<YOUR_USER_OR_ORG>/<YOUR_REPO_NAME>"
SRC_PATH = f"{REPO_ROOT}/02-transformation-silver/src"
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from utils.windowing import w_partition  # noqa: E402
from features.returns import add_log_returns  # noqa: E402
from features.ema import add_ema  # noqa: E402
from features.atr import add_atr  # noqa: E402
from features.adx import add_adx  # noqa: E402

# Load config
config_raw = dbutils.fs.head(CONFIG_PATH, 1000000)
config: Dict[str, Any] = json.loads(config_raw)

out = config["output"]

def qname(cat, sch, tbl):
    return f"{cat}.{sch}.{tbl}" if cat else f"{sch}.{tbl}"

silver_bars = qname(out.get("catalog"), out.get("schema", "market_data"), out.get("silver_bars_table", "silver_market_bars"))
silver_features = qname(out.get("catalog"), out.get("schema", "market_data"), out.get("silver_features_table", "silver_market_features"))

df = spark.table(silver_bars)

# Optional filters aligned with bars job
filters = config.get("filters", {})
if filters.get("asset_classes"):
    df = df.where(F.col("asset_class").isin(filters["asset_classes"]))
if filters.get("symbols"):
    df = df.where(F.col("symbol").isin(filters["symbols"]))
if filters.get("intervals"):
    df = df.where(F.col("bar_interval").isin(filters["intervals"]))

w = w_partition("symbol","bar_interval","ts_utc")

# Returns
lags = config.get("features", {}).get("returns", [1,3,12])
df = add_log_returns(df, w, lags=lags, price_col="close")

# EMA
ema_fast = int(config.get("features", {}).get("ema_fast", 20))
ema_slow = int(config.get("features", {}).get("ema_slow", 50))
df = add_ema(df, w, period=ema_fast, price_col="close", out_col=f"ema_fast_{ema_fast}")
df = add_ema(df, w, period=ema_slow, price_col="close", out_col=f"ema_slow_{ema_slow}")

# ATR
atr_p = int(config.get("features", {}).get("atr", 14))
df = add_atr(df, w, period=atr_p)

# Optional ADX
adx_p = config.get("features", {}).get("adx", None)
if adx_p is not None:
    df = add_adx(df, w, period=int(adx_p))

# Select output columns (match schema names for v1 defaults)
df_out = (
    df
    .select(
        "source","asset_class","symbol","bar_interval","ts_utc",
        "close",
        F.col(f"ema_fast_{ema_fast}").alias("ema_fast_20"),
        F.col(f"ema_slow_{ema_slow}").alias("ema_slow_50"),
        F.col(f"atr_{atr_p}").alias("atr_14"),
        "return_1","return_3","return_12",
        (F.col(f"adx_{int(adx_p)}").alias("adx_14") if adx_p is not None else F.lit(None).cast("double").alias("adx_14")),
        "data_quality_flag"
    )
    .withColumn("calculated_at_utc", F.lit(datetime.now(timezone.utc).replace(tzinfo=None)))
)

df_out.write.mode("overwrite").format("delta").saveAsTable(silver_features)
print(f"Wrote {silver_features} rows={df_out.count()}")
