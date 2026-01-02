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
