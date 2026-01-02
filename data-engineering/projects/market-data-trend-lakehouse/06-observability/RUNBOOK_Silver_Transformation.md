# 📘 Runbook — Silver Transformation (Market Data)

This runbook documents how to **operate and troubleshoot** the Silver transformation layer for the *Market Data & Trend Analytics* lakehouse.

---

## Scope

- `silver_market_bars` — standardized bars, time-aligned, with gap/quality flags
- `silver_market_features` — reusable indicators/features (EMA, ATR, returns, optional ADX)

---

## Jobs

### 1) Silver Bars
- Reads `bronze_market_bars_raw`
- Standardizes columns (UTC, types)
- Deduplicates by `(source, asset_class, symbol, bar_interval, ts_utc)`
- Flags gaps and invalid OHLC rows
- Writes `silver_market_bars`

### 2) Silver Features
- Reads `silver_market_bars`
- Computes indicators:
  - EMA(20), EMA(50)
  - ATR(14)
  - Returns (1, 3, 12)
  - Optional ADX(14)
- Writes `silver_market_features`

---

## Troubleshooting

### Too many GAP flags
- Validate expected interval mapping
- Confirm bar close semantics from provider
- Consider market-hours logic later for non-continuous markets

### Features mostly NULL
- Not enough history (warm-up)
- Missing OHLC values
- Excess filtering in Silver Bars

### Performance slow
- Ensure partitioning is applied
- Add OPTIMIZE/ZORDER later on `(symbol, bar_interval, ts_utc)`

---

## Operational Queries (Examples)

### GAP counts by day
Group by `symbol, bar_interval, date(ts_utc)` where `data_quality_flag='GAP'`.

### Null ratios (EMA)
Count rows where `ema_fast_20 IS NULL` (expect warm-up nulls early in the series).

---

## Notes

- Silver remains **strategy-agnostic**
- Trend/regime labeling belongs to **Gold**
- All timestamps stored in **UTC**
