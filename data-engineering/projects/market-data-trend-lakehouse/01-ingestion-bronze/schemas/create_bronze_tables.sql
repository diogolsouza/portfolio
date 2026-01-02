-- create_bronze_tables.sql
-- Convenience script to create all Bronze ingestion tables.
-- Usage:
--   1) Replace placeholders:
--        ${schema}       -> e.g., market_data
--        ${catalog_dot}  -> "" or "main." (include trailing dot when present)
--   2) Run in Databricks SQL / Spark SQL.

-- Bronze raw bars
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


-- Watermarks
-- bronze_ingestion_watermarks.sql
-- Tracks per-stream watermarks for incremental ingestion.

CREATE TABLE IF NOT EXISTS ${catalog_dot}${schema}.bronze_ingestion_watermarks (
  source                STRING,
  asset_class           STRING,
  symbol                STRING,
  bar_interval          STRING,

  last_event_time_utc   TIMESTAMP,
  last_run_id           STRING,
  last_ingested_at_utc  TIMESTAMP,
  updated_at_utc        TIMESTAMP
)
USING DELTA
TBLPROPERTIES (
  delta.enableChangeDataFeed = true
);


-- Audit log
-- bronze_ingestion_audit.sql
-- Run-level audit log for observability and troubleshooting.

CREATE TABLE IF NOT EXISTS ${catalog_dot}${schema}.bronze_ingestion_audit (
  ingestion_run_id      STRING,
  source                STRING,
  mode                  STRING,
  config_path           STRING,

  started_at_utc        TIMESTAMP,
  completed_at_utc      TIMESTAMP,
  status                STRING,        -- STARTED | SUCCESS | FAILED

  assets_count          INT,
  intervals_count       INT,

  rows_fetched          BIGINT,
  rows_after_checks     BIGINT,
  rows_merged_written   BIGINT,

  min_event_time_utc    TIMESTAMP,
  max_event_time_utc    TIMESTAMP,

  error_message         STRING
)
USING DELTA
TBLPROPERTIES (
  delta.enableChangeDataFeed = true
);

