# 📘 Runbook — Bronze Ingestion (Market Data)

This runbook documents how to **operate and troubleshoot** the Bronze ingestion layer for the *Market Data & Trend Analytics* lakehouse.

---

## Scope

Applies to the following Delta tables:

- `bronze_market_bars_raw` — canonical raw bars table (append + idempotent merge)
- `bronze_ingestion_watermarks` — per-stream high-water marks for incremental ingestion
- `bronze_ingestion_audit` — run-level audit trail and metrics

---

## Normal Operations

### Scheduled micro-batch
- Runs on a fixed cadence (e.g., every 5 minutes)
- Mode: `incremental`
- Reads the watermark per `(source, asset_class, symbol, bar_interval)`
- Fetches new data from the provider (if supported)
- Writes into `bronze_market_bars_raw` using an idempotent `MERGE`
- Updates `bronze_ingestion_watermarks` with the latest `event_time_utc`
- Records a run in `bronze_ingestion_audit`

### Manual backfill
- Triggered on-demand
- Mode: `backfill`
- Typically uses a separate config file (e.g., `ingestion.backfill.json`)
- Should be executed with care to avoid provider rate limits
- Uses the same table contracts and merge semantics

---

## What “Good” Looks Like

### Audit status
A successful run has:
- `status = 'SUCCESS'`
- `completed_at_utc` populated
- `rows_after_checks > 0` (or 0 if no new data)
- `min_event_time_utc` / `max_event_time_utc` populated when rows were written

### Watermark progress
For each `(source, asset_class, symbol, bar_interval)` you should see:
- `last_event_time_utc` steadily increasing over time
- `last_run_id` matching recent successful runs

---

## Troubleshooting Guide

### 1) Run failed (`status = 'FAILED'`)
**Symptoms**
- Latest entry in `bronze_ingestion_audit` shows `FAILED`
- `error_message` contains the failure details

**Actions**
1. Locate the failed run:
   - Filter `bronze_ingestion_audit` by `status = 'FAILED'` and sort by `started_at_utc` desc
2. Validate the job parameters:
   - `config_path`, `mode`, `as_of_utc`
3. Check provider credentials:
   - Key Vault secret scopes / keys
4. Retry:
   - If the failure was transient (timeouts, rate limits), re-run the job
5. If repeated failures occur:
   - Reduce asset list / intervals (temporary)
   - Implement exponential backoff in provider client

---

### 2) No data written (`rows_after_checks = 0`)
**Common causes**
- Provider returned no new bars (normal)
- Watermark is ahead of provider data (clock mismatch)
- Data failed Bronze sanity checks (OHLC constraints)

**Actions**
- Inspect `rows_fetched` in audit:
  - If `rows_fetched = 0`, provider returned nothing
  - If `rows_fetched > 0` but `rows_after_checks = 0`, data was filtered out by checks
- For filtered data:
  - Sample records before checks (in notebook) to see which rule is failing
  - Confirm timezone conversion and bar close semantics from provider

---

### 3) Duplicate data
**Expected behavior**
- Duplicates should be prevented by the `MERGE` key:
  `(source, asset_class, symbol, bar_interval, event_time_utc)`

**Actions**
- Verify merge condition is unchanged
- Confirm provider is not changing timestamps for the same bar (e.g., final vs preliminary bars)
- If provider revises bars:
  - The `MERGE WHEN MATCHED THEN UPDATE` will overwrite values for the same key (intended)

---

### 4) Watermark not updating
**Symptoms**
- Audit shows `SUCCESS` but watermark stays stale

**Actions**
- Ensure `rows_after_checks > 0` (watermarks update only when data exists)
- Verify watermark merge is running (notebook path/version)
- Confirm groupBy key matches the Bronze key fields

---

### 5) Performance issues / slow merges
**Actions**
- Verify partitioning is correct: `(asset_class, symbol, event_date)`
- Consider Z-ORDER on `(symbol, bar_interval, event_time_utc)` if needed (later optimization)
- Use `OPTIMIZE` and `VACUUM` policies (scheduled maintenance)

---

## Operational Queries (Examples)

> Use your catalog/schema prefix as needed.

### Latest runs
- Query `bronze_ingestion_audit` ordered by `started_at_utc` desc

### Watermark status
- Query `bronze_ingestion_watermarks` ordered by `updated_at_utc` desc

### Data freshness (per symbol/interval)
- Compute `max(event_time_utc)` from `bronze_market_bars_raw` grouped by `(symbol, bar_interval)`

---

## Notes

- Bronze is intentionally **strategy-agnostic**:
  - No indicators, no signals, no ML
- All times are stored in **UTC**
- Gap detection and time alignment are performed in **Silver**
