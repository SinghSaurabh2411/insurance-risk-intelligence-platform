# Data Dictionary

## Version

| Item | Value |
|------|------|
| Version | 1.1 |
| Status | Frozen |
| Last Updated | 27-Sep-2026 |
| Author | Saurabh Singh |

---

# Purpose

This document defines the metadata and lineage standards for the Insurance Risk Intelligence Platform.

It provides:

- Business meaning of source attributes
- Data type mappings
- Bronze, Silver and Gold layer lineage
- Data quality expectations
- Transformation requirements
- Usage within reporting, analytics and AI workloads

The accompanying Excel workbook remains the authoritative source-level metadata repository. This Markdown document records the current warehouse architecture and implementation decisions.

---

# Data Warehouse Layers

| Layer | Purpose |
|---------|----------|
| Bronze | Source preservation with required technical type conversions, complete record lineage and file-level incremental control |
| Silver | Validated, standardized and subject-oriented projections at the business observation grain |
| Gold | Dimensional model (Dimensions and Facts) targeted for reporting, analytics and downstream applications |

---

# Business Grain

The frozen business observation grain is:

~~~text
(ID_POLICY, ID_INSURED, PERIOD)
~~~

This identifies one insured individual under one policy for one observation period.

---

# Silver Subject Areas

The current Silver model contains eight tables:

| Silver Table | Subject Area |
|--------------|--------------|
| SILVER_RECORD | Record identity and technical lineage |
| SILVER_TIME | Observation and calendar attributes |
| SILVER_POLICY | Policy attributes |
| SILVER_CUSTOMER | Insured-person attributes |
| SILVER_PRODUCT | Insurance product attributes |
| SILVER_CHANNEL | Distribution channel |
| SILVER_COVERAGE | Coverage and utilization measures |
| SILVER_FINANCIAL | Policy financial measures |

### Important mapping decisions

- REIMBURSEMENT → SILVER_PRODUCT
- COST_CLAIMS_YEAR → SILVER_FINANCIAL
- N_MEDICAL_SERVICES → SILVER_COVERAGE
- Research-enrichment/contextual attributes remain Bronze-only in the current Silver design.
- No separate SILVER_CLAIMS table is introduced because the source does not provide a separate claim-level business grain.
- No separate SILVER_ENRICHMENT table is introduced because enrichment is a processing/domain concept rather than a sufficiently justified business entity.

---

# Silver Loading Standard

Silver is planned to use Oracle MERGE/upsert processing at the frozen business observation grain:

~~~text
(ID_POLICY, ID_INSURED, PERIOD)
~~~

The intended behavior is:

- matched business observation → update the current Silver representation
- unmatched business observation → insert a new Silver row

This is an incremental current-state maintenance pattern.

**MERGE/upsert is not SCD Type 2.**

SCD Type 2 requires preservation of historical versions with temporal/current-row handling. It will be evaluated for Gold dimensions when the business requirement warrants it.

---

# Bronze Loading Standard

Bronze is implemented using:

- Complete source-file SHA-256
- ETL_CONTROL lookup using SOURCE_FILE + SOURCE_FILE_HASH
- Skip when the exact source-file version has already completed successfully
- Append persistence into BRONZE_POLICY_DATA

This is file-level incremental processing, not record-level MERGE.

---

# Data Quality Standards

The following validations apply across the warehouse:

| Category | Rule |
|-----------|------|
| IDs | Must be unique where applicable |
| Dates | Valid Oracle DATE values |
| Numeric values | Must conform to documented source/business expectations |
| Nullable fields | Only fields explicitly permitted to be NULL may contain NULL |
| Enumerations | Must conform to documented source values |
| Business grain | (ID_POLICY, ID_INSURED, PERIOD) integrity must be maintained |
| Lineage | Source and load lineage must remain traceable |

---

# Transformation Standards

General ETL principles:

- Preserve source business keys.
- Standardize Oracle datatypes.
- Convert source dates to Oracle DATE.
- Preserve complete source-record lineage.
- Keep research-enrichment attributes in Bronze unless a future business requirement justifies a Silver subject area.
- Do not create separate entities solely to hold leftover columns.
- Maintain end-to-end lineage from Bronze to Gold.
- Apply Silver MERGE/upsert at the documented business grain.
- Do not treat Silver MERGE/upsert as SCD Type 2.

---

# Gold Objects

## Dimensions

~~~text
DIM_CUSTOMER
DIM_POLICY
DIM_PRODUCT
DIM_CHANNEL
DIM_TIME
~~~

## Facts

~~~text
FACT_POLICY
FACT_CLAIMS
~~~

FACT_CLAIMS remains a future design decision because the source does not contain a separate claim-level business grain.

---

# Planned Platform Components

The target architecture includes:

- **Apache Airflow** — planned orchestration layer
- **FastAPI** — planned API/service layer
- **Streamlit** — planned dashboard/application layer
- **RAG** — planned GenAI retrieval capability
- **NL2SQL** — planned natural-language query capability

These components are intentionally documented as planned until corresponding implementation exists in the repository.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 28-Jun-2026 | Initial frozen source metadata version |
| 1.1 | 27-Sep-2026 | Reconciled current eight-table Silver architecture, Silver MERGE/upsert strategy, and planned downstream component status |
