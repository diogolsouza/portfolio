# 🟡 Gold Layer — Trend & Signal Contracts

The Gold layer represents the **final, decision-ready layer** of the Market Data Lakehouse.

It converts standardized Silver features into **explainable, auditable trend and signal contracts**, designed to be consumed by analytics, BI, ML systems, or downstream execution engines.

Gold introduces **domain logic**, while remaining:
- Execution-agnostic
- Deterministic (Rules v1 baseline)
- Config-driven (asset & interval agnostic)
- Suitable for personal decision support and analytics

---

## Purpose

- Convert technical indicators into **stable trend signals**
- Provide a **single record per bar** for downstream consumption
- Serve as the **contract boundary** between data and execution
- Support future ML enrichment without breaking existing consumers

---

## Core Gold Contracts (Generic)

Gold outputs are implemented as **generic tables across assets and bar intervals**.

### 1️⃣ `gold_trend_rules`
Deterministic, rules-based trend classification.

- Baseline signal: **Rules v1**
- Fully explainable
- Auditable and reproducible

**Key fields**
- `source`
- `asset_class`
- `symbol`
- `bar_interval`
- `as_of_ts_utc`
- `trend` (UP / DOWN / FLAT)
- `trend_strength`
- `ema_fast`
- `ema_slow`
- `atr`
- `signal_version`

---

### 2️⃣ `gold_trend_ml` *(optional / placeholder)*
Reserved contract for probabilistic ML-based trend inference.

- Provides probabilities (`p_up`, `p_down`, `p_flat`)
- ML **does not replace rules**
- Designed for confidence scoring and trade filtering

This table may be empty until ML models are introduced.

---

### 3️⃣ `gold_signal_snapshot`
**Decision-ready snapshot** with one record per bar.

This is the **primary downstream consumption contract**.

**Key fields**
- `ts_utc`
- `symbol`
- `bar_interval`
- `trend_rules`
- `trend_ml` (nullable)
- `confidence`
- `trend_strength`
- `volatility_state`
- `signal_version`

Downstream systems should consume **this table**, not individual indicator tables.

---

## Rules-Based Baseline (Rules v1)

The minimum viable, explainable trend signal is defined as:

**UP**
- `ema_fast > ema_slow`
- `(ema_fast - ema_slow) / atr ≥ S_min`

**DOWN**
- `ema_fast < ema_slow`
- `(ema_fast - ema_slow) / atr ≤ -S_min`

**Else**
- `FLAT`

Where:
- `S_min` is a configurable minimum strength threshold
- `trend_strength = abs((ema_fast - ema_slow) / atr)`

This baseline alone is sufficient for **personal analytics and decision support**.

---

## Generic Design & Interval Views

Gold logic is **interval-agnostic** by design.

To provide clear, concrete outputs, **interval-specific SQL views** are exposed, for example:

- `gold_trend_5m_rules`
- `gold_trend_5m_ml`
- `gold_signal_snapshot_5m`

These are simple filters over the generic tables:
```sql
WHERE bar_interval = '5m'
```

This preserves:
- Reusability
- Architectural consistency
- Clean downstream contracts

---

## Folder Structure

```
03-serving-gold/
│
├─ config/        # Gold configuration (rules, thresholds, intervals)
├─ notebooks/     # Gold transformations (rules, snapshot, ML stub)
├─ schemas/       # Delta table & view definitions
├─ src/           # Reusable rules, confidence & volatility logic
└─ README.md
```

---

## Out of Scope

- Trade execution
- Order management
- Risk management
- Brokerage connectivity

Gold produces **signals**, not trades.

---

## Design Philosophy

- Rules-first, ML-second
- Explainability over complexity
- Contracts over ad-hoc outputs
- Stability over optimization
