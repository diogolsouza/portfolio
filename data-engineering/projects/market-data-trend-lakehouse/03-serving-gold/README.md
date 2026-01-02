# 🟡 Gold Layer — Generic Trend & Signal Contracts (Rules v1)

This Gold layer keeps the **same design strategy as Bronze/Silver**:
- **Asset- and interval-agnostic**
- **Config-driven**
- **Deterministic and auditable** (Rules v1 baseline)
- ML remains **optional** and **does not replace rules**

## Core Contracts (Generic)

1) `gold_trend_rules`
- Deterministic rules-based trend per `(source, asset_class, symbol, bar_interval, ts_utc)`

2) `gold_trend_ml` (optional / placeholder)
- Reserved contract for probabilistic ML outputs

3) `gold_signal_snapshot`
- Decision-ready contract (one row per bar), merging rules + optional ML + confidence + volatility state

## Optional Convenience Views (5m example)

For presentation purposes, you can create views such as:
- `gold_trend_5m_rules`
- `gold_trend_5m_ml`
- `gold_signal_snapshot_5m`

These are simple filters over the generic tables where `bar_interval = '5m'`.

## Inputs
- `silver_market_features`
