-- bronze_market_bars_raw.sql
-- Creates the canonical Bronze table for raw market bar ingestion (asset- and interval-agnostic).

CREATE TABLE IF NOT EXISTS ${catalog_dot}${schema}.bronze_market_bars_raw (
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
PARTITIONED BY (asset_class, symbol, event_date);
