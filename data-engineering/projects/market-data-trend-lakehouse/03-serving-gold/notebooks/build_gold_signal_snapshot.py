# Databricks notebook: build_gold_signal_snapshot.py
# Builds gold_signal_snapshot from gold_trend_rules + optional gold_trend_ml (generic for intervals).

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict

from pyspark.sql import functions as F
from pyspark.sql import Window

dbutils.widgets.text("config_path", "dbfs:/FileStore/market-data/config/gold_rules_v1_generic.json")
CONFIG_PATH = dbutils.widgets.get("config_path")

REPO_ROOT = "/Workspace/Repos/<YOUR_USER_OR_ORG>/<YOUR_REPO_NAME>"
SRC_PATH = f"{REPO_ROOT}/03-serving-gold-generic/src"
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from snapshot.volatility_state import add_volatility_state  # noqa: E402
from snapshot.confidence import add_rules_confidence  # noqa: E402

config_raw = dbutils.fs.head(CONFIG_PATH, 1000000)
config: Dict[str, Any] = json.loads(config_raw)

out = config["output"]
flt = config.get("filters", {})
rules = config["rules_v1"]
snap = config.get("snapshot", {})

def qname(cat, sch, tbl):
    return f"{cat}.{sch}.{tbl}" if cat else f"{sch}.{tbl}"

catalog = out.get("catalog")
schema = out.get("schema","market_data")

gold_rules = qname(catalog, schema, out.get("gold_rules_table","gold_trend_rules"))
gold_ml = qname(catalog, schema, out.get("gold_ml_table","gold_trend_ml"))
gold_snap = qname(catalog, schema, out.get("gold_snapshot_table","gold_signal_snapshot"))

rules_df = spark.table(gold_rules)

# Align filters
if flt.get("asset_classes"):
    rules_df = rules_df.where(F.col("asset_class").isin(flt["asset_classes"]))
if flt.get("symbols"):
    rules_df = rules_df.where(F.col("symbol").isin(flt["symbols"]))
if flt.get("intervals"):
    rules_df = rules_df.where(F.col("bar_interval").isin(flt["intervals"]))

try:
    ml_df = spark.table(gold_ml)
except Exception:
    ml_df = spark.createDataFrame(
        [],
        "source string, asset_class string, symbol string, bar_interval string, as_of_ts_utc timestamp, trend_ml string, p_up double, p_down double, p_flat double, model_version string, feature_set_version string, calculated_at_utc timestamp"
    )

if flt.get("asset_classes"):
    ml_df = ml_df.where(F.col("asset_class").isin(flt["asset_classes"]))
if flt.get("symbols"):
    ml_df = ml_df.where(F.col("symbol").isin(flt["symbols"]))
if flt.get("intervals"):
    ml_df = ml_df.where(F.col("bar_interval").isin(flt["intervals"]))

df = (
    rules_df.alias("r")
    .join(
        ml_df.select(
            "source","asset_class","symbol","bar_interval","as_of_ts_utc",
            "trend_ml","p_up","p_down","p_flat","model_version"
        ).alias("m"),
        on=["source","asset_class","symbol","bar_interval","as_of_ts_utc"],
        how="left"
    )
)

# ML confidence if available
df = df.withColumn("__ml_conf", F.greatest(F.col("p_up"), F.col("p_down"), F.col("p_flat")))

# Rules confidence proxy
s_min = float(rules.get("S_min", 0.25))
conf_cfg = snap.get("confidence_from_rules", {"enabled": True, "scale_mult": 2.0, "cap_at": 1.0})
if bool(conf_cfg.get("enabled", True)):
    df = add_rules_confidence(
        df,
        strength_col="trend_strength",
        s_min=s_min,
        scale_mult=float(conf_cfg.get("scale_mult", 2.0)),
        cap_at=float(conf_cfg.get("cap_at", 1.0)),
        out_col="__rules_conf"
    )
else:
    df = df.withColumn("__rules_conf", F.lit(None).cast("double"))

df = df.withColumn("confidence", F.coalesce(F.col("__ml_conf"), F.col("__rules_conf"))).drop("__ml_conf","__rules_conf")

# Volatility state (per symbol+interval)
w = Window.partitionBy("symbol","bar_interval").orderBy("as_of_ts_utc")
window_bars = int(snap.get("volatility_window_bars", 288))
low_mult = float(snap.get("low_mult", 0.8))
high_mult = float(snap.get("high_mult", 1.2))

df = add_volatility_state(df, w=w, atr_col="atr", window_bars=window_bars, low_mult=low_mult, high_mult=high_mult, out_col="volatility_state")

# Signal version composition
signal_version = rules.get("signal_version","rules_v1")
df = df.withColumn(
    "signal_version",
    F.when(F.col("model_version").isNotNull(), F.concat(F.lit(signal_version), F.lit("+"), F.col("model_version")))
     .otherwise(F.lit(signal_version))
)

calculated_at = datetime.now(timezone.utc).replace(tzinfo=None)

out_df = df.select(
    "source","asset_class","symbol","bar_interval",
    F.col("as_of_ts_utc").alias("ts_utc"),
    F.col("trend").alias("trend_rules"),
    "trend_ml",
    "confidence",
    "trend_strength",
    "volatility_state",
    "signal_version"
).withColumn("calculated_at_utc", F.lit(calculated_at))

out_df.write.mode("overwrite").format("delta").saveAsTable(gold_snap)
print(f"Wrote {gold_snap} rows={out_df.count()}")
