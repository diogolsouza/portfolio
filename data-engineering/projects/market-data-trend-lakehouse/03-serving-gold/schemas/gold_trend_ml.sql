-- gold_trend_ml.sql
-- Optional ML trend outputs (reserved contract). ML does not replace rules.

CREATE TABLE IF NOT EXISTS ${catalog_dot}${schema}.gold_trend_ml (
  source               STRING,
  asset_class          STRING,
  symbol               STRING,
  bar_interval         STRING,

  as_of_ts_utc         TIMESTAMP,

  trend_ml             STRING,   -- UP | DOWN | FLAT
  p_up                 DOUBLE,
  p_down               DOUBLE,
  p_flat               DOUBLE,

  model_version        STRING,
  feature_set_version  STRING,
  calculated_at_utc    TIMESTAMP
)
USING DELTA
PARTITIONED BY (asset_class, symbol, bar_interval);
