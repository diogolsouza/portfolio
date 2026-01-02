# 📚 Documentation & Governance

## Purpose

The Documentation layer centralizes **non-executable artifacts** that describe the **data model, lineage, governance, and business semantics** of the CMS Healthcare Lakehouse.

This folder complements the executable layers (Bronze, Silver, Gold) by providing **human-readable reference material** for engineers, analysts, and stakeholders.

---

## Scope of Documentation

This layer includes:

- Data dictionaries and schema references
- Business definitions and KPI descriptions
- Data lineage and flow documentation
- Governance and compliance notes
- Assumptions, limitations, and design decisions

It does **not** contain code, pipelines, or notebooks.

---

## Contents

### 📘 Data Dictionary
- Column-level definitions for Silver and Gold tables
- Business meaning, data types, and constraints
- Source-to-target mappings where applicable

### 🧭 Data Lineage
- High-level lineage from CMS source files to Gold datasets
- Layer-by-layer data flow descriptions
- Key transformation milestones

### 📐 Modeling Decisions
- Grain definitions for fact tables
- Dimension design rationale
- Surrogate vs natural key strategy

### 📊 KPI & Metric Definitions
- Formal definitions of analytical metrics
- Calculation logic (business-level, not SQL)
- Intended usage and limitations

### 🛡 Governance & Compliance Notes
- Public data usage considerations
- Data sensitivity classification (non-PHI)
- Retention and versioning assumptions

---

## Design Principles

- Documentation reflects **what is implemented**, not aspirations
- Business definitions are separated from technical logic
- Content is concise, accurate, and version-controlled
- Avoid duplication with README files in other layers

---

## Intended Audience

This documentation is intended for:

- Data Engineers
- Analytics Engineers
- BI Developers
- Data Architects
- Reviewers and auditors

It provides **context and clarity**, not execution instructions.

---

## Relationship to Other Layers

- **Bronze / Silver / Gold READMEs** describe *how* data is processed
- **This folder documents *what* the data represents and *why***

Together, they form a complete, auditable platform narrative.
