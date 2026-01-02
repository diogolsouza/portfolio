# Databricks notebook: 02-transformation-silver/notebooks/transform_silver_market_bars.py
# Purpose: Build silver_market_bars from bronze_market_bars_raw (standardization + gap flags).

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
from quality.continuity_checks import interval_to_seconds  # noqa: E402
from quality.gap_detection import add_gap_flag  # noqa: E402
from quality.constraints import enforce_ohlc_sanity  # noqa: E402

# Load config
config_raw = dbutils.fs.head(CONFIG_PATH, 1000000)
config: Dict[str, Any] = json.loads(config_raw)

inp = config["input"]
out = config["output"]

def qname(cat, sch, tbl):
    return f"{cat}.{sch}.{tbl}" if cat else f"{sch}.{tbl}"

bronze = qname(inp.get("catalog"), inp.get("schema", "market_data"), inp.get("bronze_table", "bronze_market_bars_raw"))
silver_bars = qname(out.get("catalog"), out.get("schema", "market_data"), out.get("silver_bars_table", "silver_market_bars"))

df = spark.table(bronze)

# Optional filters (portfolio-friendly)
filters = config.get("filters", {})
if filters.get("asset_classes"):
    df = df.where(F.col("asset_class").isin(filters["asset_classes"]))
if filters.get("symbols"):
    df = df.where(F.col("symbol").isin(filters["symbols"]))
if filters.get("intervals"):
    df = df.where(F.col("bar_interval").isin(filters["intervals"]))

# Standardize + rename event time
df = (
    df
    .withColumnRenamed("event_time_utc", "ts_utc")
    .dropDuplicates(["source", "asset_class", "symbol", "bar_interval", "ts_utc"])
    .select(
        "source","asset_class","symbol","bar_interval","ts_utc",
        "open","high","low","close","volume","ingested_at_utc"
    )
)

# Gap detection per interval (simple and reliable)
w = w_partition("symbol","bar_interval","ts_utc")
tol = float(config.get("quality", {}).get("gap_detection", {}).get("tolerance_multiplier", 1.05))

intervals = [r["bar_interval"] for r in df.select("bar_interval").distinct().collect()]
parts = []
for interval in intervals:
    sec = interval_to_seconds(interval)
    part = df.where(F.col("bar_interval") == interval)
    part = add_gap_flag(part, w, expected_seconds=sec, tolerance_multiplier=tol)
    parts.append(part)

df_out = parts[0]
for p in parts[1:]:
    df_out = df_out.unionByName(p)

# OHLC sanity flags (optional)
if bool(config.get("quality", {}).get("enforce_ohlc_sanity", True)):
    df_out = enforce_ohlc_sanity(df_out)
else:
    df_out = df_out.withColumn("data_quality_flag", F.lit("OK"))

df_out = df_out.withColumn("ingested_at_utc", F.coalesce(F.col("ingested_at_utc"), F.lit(datetime.now(timezone.utc).replace(tzinfo=None))))

df_out.write.mode("overwrite").format("delta").saveAsTable(silver_bars)
print(f"Wrote {silver_bars} rows={df_out.count()}")
