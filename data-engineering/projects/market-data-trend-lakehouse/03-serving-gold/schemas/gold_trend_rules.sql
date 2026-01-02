-- gold_trend_rules.sql
-- Generic rules-based trend (rules_v1). Deterministic and auditable.

CREATE TABLE IF NOT EXISTS ${catalog_dot}${schema}.gold_trend_rules (
  source              STRING,
  asset_class         STRING,
  symbol              STRING,
  bar_interval        STRING,

  as_of_ts_utc        TIMESTAMP,

  trend               STRING,   -- UP | DOWN | FLAT
  trend_strength      DOUBLE,   -- abs((ema_fast - ema_slow) / atr)
  ema_fast            DOUBLE,
  ema_slow            DOUBLE,
  atr                 DOUBLE,

  signal_version      STRING,   -- 'rules_v1'
  data_quality_flag   STRING,
  calculated_at_utc   TIMESTAMP
)
USING DELTA
PARTITIONED BY (asset_class, symbol, bar_interval);
