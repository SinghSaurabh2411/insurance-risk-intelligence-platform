# Medallion Architecture

## Purpose

This project follows the **Medallion Architecture** to organize data into progressive quality layers.

Each layer has a clearly defined responsibility:

- **Bronze** preserves the source dataset with required technical type conversions and complete source lineage.
- **Silver** stores validated, standardized, and business-oriented subject areas.
- **Gold** stores dimensional models and fact tables optimized for analytics and downstream applications.

The current implementation status is documented separately from the target architecture. Components are not described as implemented until corresponding code exists.

---

# Architecture Overview

~~~text
                    Source Dataset (CSV)
                            │
                    PySpark Bronze ETL
                            │
                            ▼
                 BRONZE_POLICY_DATA
                            │
                    PySpark Silver ETL
                            │
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼              ▼
 SILVER_RECORD  SILVER_TIME  SILVER_POLICY  SILVER_CUSTOMER  SILVER_PRODUCT
      │              │              │              │              │
      ├──────────────┼──────────────┼──────────────┤
      ▼              ▼              ▼
 SILVER_CHANNEL  SILVER_COVERAGE  SILVER_FINANCIAL
                            │
                    PySpark Gold ETL
                            │
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼              ▼
 DIM_POLICY     DIM_CUSTOMER   DIM_PRODUCT   DIM_CHANNEL     DIM_TIME
      │
      ├──────────────┐
      ▼              ▼
 FACT_POLICY      FACT_CLAIMS
                            │
                  Planned downstream consumers
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          FastAPI       Streamlit      RAG / NL2SQL
~~~

---

# Bronze Layer

## Purpose

The Bronze layer preserves the source dataset and its complete source-record lineage. Required technical type conversions are applied before Oracle persistence.

### Characteristics

- One table
- Source business columns retained
- Technical date and numeric type conversions
- Record-level SHA-256 hash
- ETL audit columns
- File-level incremental detection using source filename + SHA-256
- Append persistence
- No business deduplication or business enrichment

### Table

| Table |
|---------|
| BRONZE_POLICY_DATA |

---

# Silver Layer

## Purpose

The Silver layer contains validated, standardized, and logically separated subject areas. Each table represents a meaningful business/domain subject area rather than a bucket for leftover columns.

### Transformations

- Schema and data-type standardization
- Data quality validation
- Business-key and grain validation
- Null and categorical validation
- Subject-area projection
- Lineage propagation
- Incremental MERGE/upsert at the business observation grain

### Tables

| Table | Purpose |
|---------|----------|
| SILVER_RECORD | Record-level identity and technical lineage |
| SILVER_TIME | Observation period |
| SILVER_POLICY | Policy-related attributes |
| SILVER_CUSTOMER | Insured-person attributes |
| SILVER_PRODUCT | Insurance product attributes |
| SILVER_CHANNEL | Distribution-channel attributes |
| SILVER_COVERAGE | Coverage and utilization measures |
| SILVER_FINANCIAL | Policy financial measures |

COST_CLAIMS_YEAR remains a financial measure in SILVER_FINANCIAL; the source does not contain a separate claim-level business grain.

Research-enrichment/contextual attributes remain Bronze-only for the current Silver design unless a future business requirement establishes a justified subject area.

### Silver Loading Strategy

Silver is planned to use Oracle MERGE/upsert processing using the frozen business observation grain:

~~~text
(ID_POLICY, ID_INSURED, PERIOD)
~~~

Conceptually:

~~~text
Bronze observation
      │
      ▼
Validate / standardize
      │
      ▼
Match Silver on business grain
      │
      ├── matched     → UPDATE
      │
      └── not matched → INSERT
~~~

This maintains the current validated Silver representation of each business observation. **MERGE/upsert is not SCD Type 2.**

A true SCD Type 2 implementation requires historical versions and temporal/current-row handling. SCD Type 2 will be evaluated later for Gold dimensions where the business requirement justifies historical tracking.

---

# Gold Layer

## Purpose

The Gold layer provides analytics-ready dimensional models.

### Dimension Tables

| Dimension | Description |
|------------|-------------|
| DIM_POLICY | Policy information |
| DIM_CUSTOMER | Customer information |
| DIM_PRODUCT | Product information |
| DIM_CHANNEL | Distribution channel |
| DIM_TIME | Calendar dimension |

### Fact Tables

| Fact | Description |
|------|-------------|
| FACT_POLICY | Policy metrics |
| FACT_CLAIMS | Claims-related fact; exact business grain remains a future design decision |

Gold is not yet described as implemented until corresponding code and DDL exist.

---

# Planned Downstream Consumers

The target architecture includes:

- **FastAPI** — planned API/service layer
- **Streamlit** — planned analytics/dashboard layer
- **RAG** — planned retrieval-augmented generation capability
- **NL2SQL** — planned natural-language-to-SQL capability

These are target architecture components and are not currently treated as implemented.

---

# Incremental Loading Strategy

The project uses different incremental strategies by layer.

### Bronze

Bronze uses:

~~~text
SOURCE_FILE + SHA-256
~~~

If the same source filename and complete-file SHA-256 hash have already completed successfully, the source version is skipped. Otherwise it is processed and persisted using append.

### Silver

Silver is planned to use Oracle MERGE/upsert at:

~~~text
(ID_POLICY, ID_INSURED, PERIOD)
~~~

This is business-grain current-state maintenance and is distinct from SCD Type 2.

### Gold

Gold loading and historical dimension strategies remain future implementation decisions. SCD Type 2 will be applied only where the dimensional business requirement justifies it.

---

# Data Quality Responsibilities

| Layer | Responsibility |
|---------|----------------|
| Bronze | Source preservation, technical validation, lineage and file-level incremental control |
| Silver | Validation, standardization, business-grain integrity and subject-area separation |
| Gold | Analytics-ready dimensional modeling and business measures |

---

# Design Principles

- Preserve source business keys.
- Keep the frozen business observation grain explicit.
- Separate business/domain subject areas without creating unnecessary entities.
- Do not introduce a Silver claims or enrichment entity without a justified business grain.
- Preserve complete source-record lineage.
- Use Bronze append + file-hash detection.
- Use planned Silver MERGE/upsert at the business grain.
- Do not equate MERGE/upsert with SCD Type 2.
- Apply SCD Type 2 only where a future Gold dimensional requirement justifies it.
- Document planned components as planned until their implementation exists.

---

# Frozen Design Decisions

| Decision | Status |
|-----------|--------|
| Architecture | Medallion |
| ETL Engine | PySpark |
| Database | Oracle 21c XE |
| Bronze Incremental Detection | SOURCE_FILE + SHA-256 |
| Bronze Write Strategy | APPEND |
| Business Grain | (ID_POLICY, ID_INSURED, PERIOD) |
| Bronze Table | BRONZE_POLICY_DATA |
| Silver Tables | 8 subject-oriented tables |
| Silver Write Strategy | MERGE / UPSERT — planned |
| Silver MERGE Key | (ID_POLICY, ID_INSURED, PERIOD) |
| SCD Type 2 | Future Gold design decision where justified |
| Gold Layer | Star Schema |
| Airflow | Planned orchestration layer |
| FastAPI | Planned API/service layer |
| Streamlit | Planned dashboard/application layer |
| RAG | Planned GenAI retrieval capability |
| NL2SQL | Planned natural-language query capability |
