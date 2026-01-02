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
