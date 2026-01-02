# ⚪ Transformation — Silver Layer

## Purpose

The Silver layer is responsible for **standardizing, validating, and enriching** raw market data ingested in Bronze into **analysis-ready, time-aligned time-series datasets**.

It serves as the **canonical foundation for analytics and feature generation**, while remaining **strategy- and execution-agnostic**.

---

## Responsibilities

- Standardize schemas and data types
- Normalize timestamps and time zones
- Enforce consistent asset and interval representations
- Perform **time-series alignment and gap detection**
- Generate **reusable, domain-agnostic features**
- Apply deterministic data quality rules

---

## What This Layer Is (and Is Not)

### This layer **does**
- Create clean, validated time-series datasets
- Produce reusable numerical features (e.g., returns, volatility)
- Flag data quality issues (gaps, anomalies)
- Support reproducible analytics and ML workloads

### This layer **does not**
- Generate trading signals
- Perform trend classification or regime labeling
- Make execution or position decisions
- Contain broker- or strategy-specific logic

Those responsibilities belong to **Gold or downstream consumers**.

---

## Input Sources

- `bronze_market_bars_raw`

Silver consumes **only Bronze data**, preserving the Medallion contract.

---

## Core Transformations

### 1) Standardization
- Enforce canonical data types and precision
- Normalize:
  - `asset_class`
  - `symbol`
  - `bar_interval`
- Convert all timestamps to **UTC**
- Ensure deterministic ordering by `(symbol, interval, event_time_utc)`

---

### 2) Time Alignment & Gap Detection
- Align data to expected bar intervals
- Detect missing or irregular bars
- Flag gaps without imputing values
- Preserve raw values while surfacing data quality signals

Gap handling is **explicit and observable**, not implicit.

---

### 3) Feature Engineering (Reusable Only)

Silver generates **general-purpose features**, including:
- Log and simple returns
- Rolling volatility
- Moving averages (SMA / EMA)
- Range-based measures (e.g., ATR)

Features are:
- Deterministic
- Parameterized
- Reusable across strategies and analytics

---

## Output Tables

### Core Tables
- `silver_market_bars` — standardized, time-aligned OHLC series
- `silver_market_features` — reusable numerical features

### Quality Signals
- Gap flags
- Outlier indicators
- Completeness metrics

No signal labels or predictions are produced in Silver.

---

## Data Quality Rules

Silver enforces:
- Uniqueness of `(source, asset_class, symbol, bar_interval, event_time_utc)`
- Time continuity expectations
- Numeric sanity (non-negative volumes, valid price ranges)
- Feature calculation validity (no silent NaNs)

Quality results are surfaced to the **Observability layer**.

---

## Design Principles

- Deterministic and reproducible transformations
- Clear separation from Bronze and Gold responsibilities
- Asset- and timeframe-agnostic logic
- Optimized for analytics and ML readiness

---

## Downstream Dependencies

Silver outputs are consumed by the **Gold serving layer**, where:
- Trends
- Regimes
- Signals
- Aggregations

are derived for analytics and downstream use cases.
