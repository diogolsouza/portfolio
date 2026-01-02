-- silver_market_bars.sql
-- Canonical standardized, time-aligned bar series with quality flags.

CREATE TABLE IF NOT EXISTS ${catalog_dot}${schema}.silver_market_bars (
  source            STRING,
  asset_class       STRING,
  symbol            STRING,
  bar_interval      STRING,

  ts_utc            TIMESTAMP,

  open              DOUBLE,
  high              DOUBLE,
  low               DOUBLE,
  close             DOUBLE,
  volume            DOUBLE,

  data_quality_flag STRING,   -- OK | GAP | DUPLICATE | OUT_OF_ORDER | INVALID_OHLC

  ingested_at_utc   TIMESTAMP
)
USING DELTA
PARTITIONED BY (asset_class, symbol, bar_interval);
