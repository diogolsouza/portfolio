# ⚪ Transformation — Silver Layer

## Purpose

The Silver layer is responsible for **standardizing, validating, and enriching** raw market data into **analysis-ready time-series datasets**.

This layer bridges raw ingestion and analytical signal generation.

---

## Responsibilities

- Normalize timestamps and time zones
- Enforce schema consistency
- Detect and handle missing or irregular intervals
- Apply data quality rules
- Generate reusable time-series features

---

## Key Transformations

- Time alignment and gap detection
- Numeric normalization and precision handling
- Return and volatility calculations
- Volume and liquidity feature derivation
- Asset- and timeframe-agnostic processing

---

## Core Silver Tables

- `silver_market_bars`
- `silver_market_features`

Each table represents a **clean, validated, and standardized** time-series dataset.

---

## Data Quality Checks

Implemented checks include:
- Timestamp continuity
- Duplicate detection
- Null and range validation
- Volume and price sanity checks

Quality results are surfaced to the **Observability layer**.

---

## Downstream Dependencies

Silver datasets are consumed by the **Gold serving layer** to generate analytical trends and signal-oriented datasets.