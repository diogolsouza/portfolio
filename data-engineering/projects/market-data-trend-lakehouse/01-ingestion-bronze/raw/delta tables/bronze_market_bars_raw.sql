CREATE TABLE IF NOT EXISTS bronze_market_bars_raw (
  source              STRING,   -- data provider identifier
  asset_class         STRING,   -- FX | EQUITY | ETF | CRYPTO | INDEX | etc.
  symbol              STRING,   -- normalized instrument symbol
  bar_interval        STRING,   -- 1m | 5m | 15m | 1h | 1d (configurable)
  event_time_utc      TIMESTAMP, -- bar close time in UTC (event-time)
  open                DOUBLE,
  high                DOUBLE,
  low                 DOUBLE,
  close               DOUBLE,
  volume              DOUBLE,    -- tick volume or real volume depending on source
  source_event_time   TIMESTAMP, -- optional: original source time if different
  source_payload      STRING,    -- optional: raw JSON string (only if you want full fidelity)
  ingested_at_utc     TIMESTAMP,
  ingestion_run_id    STRING,
  source_batch_id     STRING,    -- optional: file name / API batch / pagination token
  record_hash         STRING     -- optional: hash for idempotency across variations
)
USING DELTA
PARTITIONED BY (asset_class, symbol, event_date);

-- event_date is derived in write step: DATE(event_time_utc)
