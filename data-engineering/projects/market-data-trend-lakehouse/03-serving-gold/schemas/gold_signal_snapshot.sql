-- gold_signal_snapshot.sql
-- Decision-ready snapshot (one record per bar) consumed by downstream systems.

CREATE TABLE IF NOT EXISTS ${catalog_dot}${schema}.gold_signal_snapshot (
  source             STRING,
  asset_class        STRING,
  symbol             STRING,
  bar_interval       STRING,

  ts_utc             TIMESTAMP,

  trend_rules        STRING,   -- UP | DOWN | FLAT
  trend_ml           STRING,   -- UP | DOWN | FLAT (nullable until ML is implemented)
  confidence         DOUBLE,   -- 0..1 (ML if available; else rule-based proxy)
  trend_strength     DOUBLE,   -- abs((ema_fast - ema_slow) / atr)

  volatility_state   STRING,   -- LOW | MED | HIGH (derived from ATR state)
  signal_version     STRING,   -- e.g., 'rules_v1' or 'rules_v1+ml_vX'

  calculated_at_utc  TIMESTAMP
)
USING DELTA
PARTITIONED BY (asset_class, symbol, bar_interval);
