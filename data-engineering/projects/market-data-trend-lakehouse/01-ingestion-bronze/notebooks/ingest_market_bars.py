# Databricks notebook: 01-ingestion-bronze/notebooks/ingest_market_bars.py
# Purpose: Ingest raw market bars into bronze_market_bars_raw (Delta), using a provider-agnostic interface.

from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, TimestampType, DoubleType, DateType
)

# -----------------------------
# 0) Parameters (Databricks job params)
# -----------------------------
dbutils.widgets.text("config_path", "dbfs:/FileStore/market-data/config/ingestion.json")
dbutils.widgets.text("as_of_utc", "")           # optional override (ISO8601), else 'now'
dbutils.widgets.text("mode", "incremental")     # incremental | backfill

CONFIG_PATH = dbutils.widgets.get("config_path")
AS_OF_UTC = dbutils.widgets.get("as_of_utc").strip() or None
MODE = dbutils.widgets.get("mode").strip().lower()

if MODE not in {"incremental", "backfill"}:
    raise ValueError("mode must be one of: incremental | backfill")

run_id = str(uuid.uuid4())
ingested_at_utc = datetime.now(timezone.utc).replace(tzinfo=None)  # store as naive UTC timestamp

# -----------------------------
# 1) Make local project modules available
#    NOTE: Update this path to match your Databricks Repo path.
# -----------------------------
# Example:
# REPO_ROOT = "/Workspace/Repos/diogo.souza@datacompound.onmicrosoft.com/market-data-trend-lakehouse"
REPO_ROOT = "/Workspace/Repos/<YOUR_USER_OR_ORG>/<YOUR_REPO_NAME>"

SRC_PATH = f"{REPO_ROOT}/01-ingestion-bronze/src"
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from providers.factory import build_provider  # noqa: E402
from utils.normalization import (             # noqa: E402
    normalize_symbol,
    normalize_asset_class,
    normalize_interval
)

# -----------------------------
# 2) Load config
# -----------------------------
config_raw = dbutils.fs.head(CONFIG_PATH, 1000000)
config: Dict[str, Any] = json.loads(config_raw)

SOURCE = config["source"]
ASSETS: List[Dict[str, str]] = config["assets"]
INTERVALS: List[str] = config["intervals"]
STORAGE: Dict[str, str] = config["storage"]

CATALOG = STORAGE.get("catalog")          # optional
SCHEMA = STORAGE.get("schema", "market_data")
BRONZE_TABLE = STORAGE.get("bronze_table", "bronze_market_bars_raw")

FULL_SCHEMA = f"{CATALOG}.{SCHEMA}" if CATALOG else SCHEMA
FULL_TABLE_NAME = f"{FULL_SCHEMA}.{BRONZE_TABLE}"

# Provider instance (factory)
provider = build_provider(SOURCE, config.get("source_options", {}))

# -----------------------------
# 3) Ensure schema & table exist (idempotent)
# -----------------------------
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {FULL_SCHEMA}")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {FULL_TABLE_NAME} (
  source              STRING,
  asset_class         STRING,
  symbol              STRING,
  bar_interval        STRING,

  event_time_utc      TIMESTAMP,
  open                DOUBLE,
  high                DOUBLE,
  low                 DOUBLE,
  close               DOUBLE,
  volume              DOUBLE,

  source_event_time   TIMESTAMP,
  source_payload      STRING,

  ingested_at_utc     TIMESTAMP,
  ingestion_run_id    STRING,
  source_batch_id     STRING,
  record_hash         STRING,

  event_date          DATE
)
USING DELTA
PARTITIONED BY (asset_class, symbol, event_date)
""")

# -----------------------------
# 4) Fetch from provider + normalize into canonical rows
# -----------------------------
rows: List[Dict[str, Any]] = []

for a in ASSETS:
    asset_class = normalize_asset_class(a["asset_class"])
    symbol = normalize_symbol(a["symbol"])

    for interval in INTERVALS:
        interval = normalize_interval(interval)

        bars = provider.fetch_bars(
            asset_class=asset_class,
            symbol=symbol,
            interval=interval,
            mode=MODE,
            as_of_utc=AS_OF_UTC,
        )

        for b in bars:
            rows.append({
                "source": provider.name(),
                "asset_class": asset_class,
                "symbol": symbol,
                "bar_interval": interval,
                "event_time_utc": b.event_time_utc,
                "open": float(b.open) if b.open is not None else None,
                "high": float(b.high) if b.high is not None else None,
                "low": float(b.low) if b.low is not None else None,
                "close": float(b.close) if b.close is not None else None,
                "volume": float(b.volume) if b.volume is not None else None,
                "source_event_time": b.source_event_time,
                "source_payload": b.source_payload,
                "ingested_at_utc": ingested_at_utc,
                "ingestion_run_id": run_id,
                "source_batch_id": b.source_batch_id,
                "record_hash": b.record_hash,
            })

schema = StructType([
    StructField("source", StringType(), False),
    StructField("asset_class", StringType(), False),
    StructField("symbol", StringType(), False),
    StructField("bar_interval", StringType(), False),

    StructField("event_time_utc", TimestampType(), False),
    StructField("open", DoubleType(), True),
    StructField("high", DoubleType(), True),
    StructField("low", DoubleType(), True),
    StructField("close", DoubleType(), True),
    StructField("volume", DoubleType(), True),

    StructField("source_event_time", TimestampType(), True),
    StructField("source_payload", StringType(), True),

    StructField("ingested_at_utc", TimestampType(), False),
    StructField("ingestion_run_id", StringType(), False),
    StructField("source_batch_id", StringType(), True),
    StructField("record_hash", StringType(), True),

    StructField("event_date", DateType(), True),  # derived
])

df = spark.createDataFrame(rows, schema=schema) if rows else spark.createDataFrame([], schema=schema)

# Derive partition column
df = df.withColumn("event_date", F.to_date(F.col("event_time_utc")))

# -----------------------------
# 5) Bronze-level checks (technical only)
# -----------------------------
df_checked = (
    df
    .filter(F.col("symbol").isNotNull())
    .filter(F.col("bar_interval").isNotNull())
    .filter(F.col("event_time_utc").isNotNull())
    .filter(F.col("high").isNull() | (F.col("high") >= F.greatest(F.col("open"), F.col("close"))))
    .filter(F.col("low").isNull()  | (F.col("low")  <= F.least(F.col("open"), F.col("close"))))
    .filter(F.col("high").isNull() | F.col("low").isNull() | (F.col("high") >= F.col("low")))
)

# Create a temp view for MERGE
df_checked.createOrReplaceTempView("staging_bars")

# -----------------------------
# 6) Idempotent merge into Bronze Delta table
# -----------------------------
spark.sql(f"""
MERGE INTO {FULL_TABLE_NAME} AS t
USING staging_bars AS s
ON  t.source = s.source
AND t.asset_class = s.asset_class
AND t.symbol = s.symbol
AND t.bar_interval = s.bar_interval
AND t.event_time_utc = s.event_time_utc
WHEN MATCHED THEN UPDATE SET
  t.open = s.open,
  t.high = s.high,
  t.low  = s.low,
  t.close = s.close,
  t.volume = s.volume,
  t.source_event_time = s.source_event_time,
  t.source_payload = s.source_payload,
  t.ingested_at_utc = s.ingested_at_utc,
  t.ingestion_run_id = s.ingestion_run_id,
  t.source_batch_id = s.source_batch_id,
  t.record_hash = s.record_hash,
  t.event_date = s.event_date
WHEN NOT MATCHED THEN INSERT *
""")

rows_in = df.count()
rows_checked = df_checked.count()

print(
    f"Bronze ingestion completed. "
    f"provider={provider.name()} mode={MODE} run_id={run_id} "
    f"rows_in={rows_in} rows_written={rows_checked} table={FULL_TABLE_NAME}"
)
