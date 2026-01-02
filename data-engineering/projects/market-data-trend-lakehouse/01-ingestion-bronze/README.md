# 🟤 Ingestion - Bronze Layer

## Purpose

The Bronze layer is responsible for the **raw ingestion of market data** into the lakehouse, preserving **source fidelity, replayability, and auditability**.

It represents the **system of record** for all downstream processing in the Market Data & Trend Analytics platform.

---

## Responsibilities

- Ingest raw market data from external providers
- Preserve original schemas, values, and event timestamps
- Support **incremental and backfill ingestion modes**
- Ensure replayability and deterministic reprocessing
- Capture ingestion metadata for traceability and observability

---

## Data Characteristics

- Domain: Financial market data
- Data type: Time-series (prices, volumes, aggregates)
- Ingestion modes:
  - Batch / backfill
  - Micro-batch (scheduled)
  - Streaming (future-compatible)
- Granularity: Configurable (e.g., minutes, hours, days)

---

## Design Principles

- No business or analytical logic applied
- No indicators, features, or signals
- Idempotent ingestion using deterministic keys
- Source-faithful schemas and timestamps
- Partitioning optimized for time-series access

---

## Ingestion Strategy

- Data is written to Delta Lake using **idempotent MERGE semantics**
- Late-arriving or revised data overwrites existing records with the same business key
- Incremental ingestion is driven by **per-stream watermarks**
- Backfills reuse the same ingestion pipeline and contracts

---

## Outputs

### Core Tables
- `bronze_market_bars_raw` — canonical raw OHLC time-series
- `bronze_ingestion_watermarks` — per-asset/interval high-water marks
- `bronze_ingestion_audit` — run-level ingestion metrics and status

### Ingestion Metadata
Each Bronze record includes:
- `ingested_at_utc`
- `ingestion_run_id`
- `source`
- `asset_class`
- `symbol`
- `bar_interval`

---

## Data Quality (Bronze-Level)

Bronze validations are **technical only**, including:
- Mandatory field presence (symbol, interval, event time)
- OHLC sanity checks (high/low bounds)
- Schema validation

Analytical validations (gap detection, alignment, statistical checks) are intentionally deferred to **Silver**.

---

## Downstream Dependencies

Data from the Bronze layer is consumed exclusively by the **Silver transformation layer**, where:
- Time alignment
- Gap detection
- Feature engineering
- Standardization

are applied.

Bronze remains **strategy- and analytics-agnostic by design**.
