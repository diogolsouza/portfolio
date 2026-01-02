# Databricks notebook: build_gold_trend_ml_stub.py
# Placeholder: refreshes gold_trend_ml with no predictions (reserved contract).

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict

from pyspark.sql import functions as F

dbutils.widgets.text("config_path", "dbfs:/FileStore/market-data/config/gold_rules_v1_generic.json")
CONFIG_PATH = dbutils.widgets.get("config_path")

config_raw = dbutils.fs.head(CONFIG_PATH, 1000000)
config: Dict[str, Any] = json.loads(config_raw)

out = config["output"]

def qname(cat, sch, tbl):
    return f"{cat}.{sch}.{tbl}" if cat else f"{sch}.{tbl}"

gold_ml = qname(out.get("catalog"), out.get("schema","market_data"), out.get("gold_ml_table","gold_trend_ml"))

empty = spark.createDataFrame(
    [],
    "source string, asset_class string, symbol string, bar_interval string, as_of_ts_utc timestamp, trend_ml string, p_up double, p_down double, p_flat double, model_version string, feature_set_version string, calculated_at_utc timestamp"
).withColumn("calculated_at_utc", F.lit(datetime.now(timezone.utc).replace(tzinfo=None)))

empty.write.mode("overwrite").format("delta").saveAsTable(gold_ml)
print(f"Refreshed {gold_ml} (empty stub)." )
