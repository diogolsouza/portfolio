# 📘 Runbook — Gold Generic Trend Contracts (Rules v1)

Contracts (generic):
- `gold_trend_rules`
- `gold_trend_ml` (optional / placeholder)
- `gold_signal_snapshot` (decision-ready contract)

All outputs are keyed by:
`(source, asset_class, symbol, bar_interval, ts_utc)`

## Rule (rules_v1)

UP:
- ema_fast > ema_slow
- (ema_fast - ema_slow) / atr >= S_min

DOWN:
- ema_fast < ema_slow
- (ema_fast - ema_slow) / atr <= -S_min

Else: FLAT

## Operational Checks
- One row per key in `gold_signal_snapshot`
- Volatility state distribution plausible (LOW/MED/HIGH)
- `trend_strength` non-null after indicator warm-up

## Presentation Views
If you want 5m-specific naming, create views filtering `bar_interval='5m'`.
