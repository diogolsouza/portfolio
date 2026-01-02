-- silver_market_features.sql
-- Reusable, strategy-agnostic time-series features/indicators calculated from silver_market_bars.

CREATE TABLE IF NOT EXISTS ${catalog_dot}${schema}.silver_market_features (
  source            STRING,
  asset_class       STRING,
  symbol            STRING,
  bar_interval      STRING,

  ts_utc            TIMESTAMP,

  close             DOUBLE,

  ema_fast_20       DOUBLE,
  ema_slow_50       DOUBLE,
  atr_14            DOUBLE,

  return_1          DOUBLE,
  return_3          DOUBLE,
  return_12         DOUBLE,

  adx_14            DOUBLE,

  data_quality_flag STRING,
  calculated_at_utc TIMESTAMP
)
USING DELTA
PARTITIONED BY (asset_class, symbol, bar_interval);
