# Databricks notebook: build_gold_trend_rules.py
# Builds gold_trend_rules from silver_market_features using rules_v1 (generic for intervals).

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict

from pyspark.sql import functions as F

dbutils.widgets.text("config_path", "dbfs:/FileStore/market-data/config/gold_rules_v1_generic.json")
CONFIG_PATH = dbutils.widgets.get("config_path")

REPO_ROOT = "/Workspace/Repos/<YOUR_USER_OR_ORG>/<YOUR_REPO_NAME>"
SRC_PATH = f"{REPO_ROOT}/03-serving-gold-generic/src"
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from rules.rules_v1 import add_rules_v1_trend  # noqa: E402

config_raw = dbutils.fs.head(CONFIG_PATH, 1000000)
config: Dict[str, Any] = json.loads(config_raw)

inp = config["input"]
out = config["output"]
flt = config.get("filters", {})
rules = config["rules_v1"]

def qname(cat, sch, tbl):
    return f"{cat}.{sch}.{tbl}" if cat else f"{sch}.{tbl}"

silver_feat = qname(inp.get("catalog"), inp.get("schema","market_data"), inp.get("silver_features_table","silver_market_features"))
gold_rules = qname(out.get("catalog"), out.get("schema","market_data"), out.get("gold_rules_table","gold_trend_rules"))

df = spark.table(silver_feat)

# Filters (align with Bronze/Silver style)
if flt.get("asset_classes"):
    df = df.where(F.col("asset_class").isin(flt["asset_classes"]))
if flt.get("symbols"):
    df = df.where(F.col("symbol").isin(flt["symbols"]))
if flt.get("intervals"):
    df = df.where(F.col("bar_interval").isin(flt["intervals"]))

ema_fast_col = rules.get("ema_fast_col","ema_fast_20")
ema_slow_col = rules.get("ema_slow_col","ema_slow_50")
atr_col = rules.get("atr_col","atr_14")
s_min = float(rules.get("S_min", 0.25))
signal_version = rules.get("signal_version","rules_v1")

df = df.select(
    "source","asset_class","symbol","bar_interval",
    F.col("ts_utc").alias("as_of_ts_utc"),
    F.col(ema_fast_col).alias("ema_fast"),
    F.col(ema_slow_col).alias("ema_slow"),
    F.col(atr_col).alias("atr"),
    "data_quality_flag"
)

df = add_rules_v1_trend(df, ema_fast_col="ema_fast", ema_slow_col="ema_slow", atr_col="atr", s_min=s_min)

calculated_at = datetime.now(timezone.utc).replace(tzinfo=None)
df_out = (
    df
    .withColumn("signal_version", F.lit(signal_version))
    .withColumn("calculated_at_utc", F.lit(calculated_at))
    .select(
        "source","asset_class","symbol","bar_interval",
        "as_of_ts_utc",
        "trend","trend_strength","ema_fast","ema_slow","atr",
        "signal_version","data_quality_flag","calculated_at_utc"
    )
)

df_out.write.mode("overwrite").format("delta").saveAsTable(gold_rules)
print(f"Wrote {gold_rules} rows={df_out.count()}")
