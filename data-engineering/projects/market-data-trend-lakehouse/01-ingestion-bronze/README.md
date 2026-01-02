# 🟤 Ingestion — Bronze Layer

## Purpose

The Bronze layer is responsible for the **raw ingestion of market data** into the lakehouse, preserving **source fidelity, replayability, and auditability**.

This layer represents the **system of record** for all downstream processing.

---

## Responsibilities

- Ingest raw market data from external sources
- Preserve original schemas and timestamps
- Append-only ingestion (no updates or deletes)
- Add ingestion metadata for traceability

---

## Data Characteristics

- Domain: Financial market data
- Data type: Time-series (prices, volumes, aggregates)
- Ingestion mode: Batch, micro-batch, or streaming
- Granularity: Configurable (e.g., minutes, hours, days)

---

## Design Principles

- No business logic applied
- No deduplication or enrichment
- Idempotent ingestion patterns
- Partitioning by asset, date, and/or source

---

## Outputs (Examples)

- `bronze_market_prices_raw`
- `bronze_market_bars_raw`

Each table includes ingestion metadata such as:
- `ingested_at`
- `source`
- `asset_class`
- `symbol`

---

## Downstream Dependencies

Data from the Bronze layer is consumed exclusively by the **Silver transformation layer**, where standardization and feature engineering are applied.
