-- Optional convenience views (presentation only)
-- These views keep your portfolio aligned with the earlier '5m contract' wording,
-- while the underlying Gold tables remain generic.

CREATE OR REPLACE VIEW ${catalog_dot}${schema}.gold_trend_5m_rules AS
SELECT * FROM ${catalog_dot}${schema}.gold_trend_rules
WHERE bar_interval = '5m';

CREATE OR REPLACE VIEW ${catalog_dot}${schema}.gold_trend_5m_ml AS
SELECT * FROM ${catalog_dot}${schema}.gold_trend_ml
WHERE bar_interval = '5m';

CREATE OR REPLACE VIEW ${catalog_dot}${schema}.gold_signal_snapshot_5m AS
SELECT * FROM ${catalog_dot}${schema}.gold_signal_snapshot
WHERE bar_interval = '5m';
