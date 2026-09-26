# Data Flow

## Purpose

This document describes the end-to-end movement of data through the platform.

The project follows a Medallion Architecture where data progresses through Bronze, Silver, and Gold layers before reaching planned downstream applications.

The currently implemented ETL engine is PySpark. **Apache Airflow is planned as the orchestration layer and is not currently treated as implemented.**

---

# End-to-End Data Flow

~~~text
Source Dataset (CSV)
        │
        ▼
PySpark Bronze ETL
        │
        ▼
BRONZE_POLICY_DATA
        │
        ▼
PySpark Silver ETL
        │
        ├── SILVER_RECORD
        ├── SILVER_TIME
        ├── SILVER_POLICY
        ├── SILVER_CUSTOMER
        ├── SILVER_PRODUCT
        ├── SILVER_CHANNEL
        ├── SILVER_COVERAGE
        └── SILVER_FINANCIAL
        │
        ▼
PySpark Gold ETL
        │
        ├── DIM_POLICY
        ├── DIM_CUSTOMER
        ├── DIM_PRODUCT
        ├── DIM_CHANNEL
        ├── DIM_TIME
        ├── FACT_POLICY
        └── FACT_CLAIMS
        │
        ▼
Planned consumers
        ├── FastAPI
        ├── Streamlit
        └── RAG / NL2SQL
~~~

---

# Data Processing Flow

~~~text
Source CSV
      │
      ▼
Bronze Layer — implemented
      │
      ▼
Silver Layer — logical design frozen; DDL/ETL pending
      │
      ▼
Gold Layer — planned implementation
      │
      ▼
Planned Analytics & AI Applications
~~~

---

# Step 1 – Source Ingestion

Input consists of the insurance policy CSV dataset.

The source dataset is treated as the source of truth for the Bronze ingestion process.

---

# Step 2 – Bronze Layer

The implemented Bronze ETL performs:

- CSV discovery and ingestion
- Source schema validation
- Technical date and numeric type conversion
- Business-key validation
- Record-level SHA-256 generation
- ETL audit-column generation
- Oracle loading into BRONZE_POLICY_DATA
- File-level incremental detection

### Bronze incremental detection

For each source file:

~~~text
Calculate complete-file SHA-256
          │
          ▼
Check ETL_CONTROL for:
SOURCE_FILE + SOURCE_FILE_HASH + SUCCESS
          │
       ┌──┴──┐
       │     │
     match  no match
       │     │
      skip  process
             │
             ▼
       Bronze APPEND
~~~

This is **file-level incremental processing**, not record-level MERGE/upsert.

---

# Step 3 – Silver Layer

The Silver layer reads the Bronze data and separates it into eight subject-oriented tables:

- SILVER_RECORD
- SILVER_TIME
- SILVER_POLICY
- SILVER_CUSTOMER
- SILVER_PRODUCT
- SILVER_CHANNEL
- SILVER_COVERAGE
- SILVER_FINANCIAL

The frozen business observation grain is:

~~~text
(ID_POLICY, ID_INSURED, PERIOD)
~~~

Silver is planned to use Oracle MERGE/upsert against this business grain:

- Existing business observation → update current Silver representation
- New business observation → insert
- Business grain remains explicit and validated

This is **not SCD Type 2**. Historical dimension versioning will be considered later for Gold dimensions where justified.

---

# Step 4 – Gold Layer

The planned Gold ETL will build a dimensional model.

Dimension tables:

- DIM_POLICY
- DIM_CUSTOMER
- DIM_PRODUCT
- DIM_CHANNEL
- DIM_TIME

Fact tables:

- FACT_POLICY
- FACT_CLAIMS

The exact FACT_CLAIMS grain remains a future design decision because the source does not contain a separate claim-level entity.

---

# Planned Data Consumption

The Gold layer is the planned source for downstream applications.

## FastAPI — Planned

Provides REST APIs for accessing dimensional and fact data after the API layer is implemented.

## Streamlit — Planned

Provides interactive dashboards after the application layer is implemented.

## RAG — Planned

Retrieves approved business metadata/documentation for natural-language assistance after the GenAI layer is implemented.

## NL2SQL — Planned

Converts natural-language questions into controlled SQL against the Gold schema after the NL2SQL capability is implemented.

These components are architectural targets, not current implementation claims.

---

# Planned Workflow Orchestration

Apache Airflow is the **planned orchestration layer**.

The target execution order is:

~~~text
CSV
 ↓
Bronze ETL
 ↓
Silver ETL
 ↓
Gold ETL
 ↓
Data Validation
 ↓
API / Dashboard / AI refresh
~~~

The current repository does not contain an implemented Airflow DAG, so Airflow is not described as an active production component.

---

# Error Handling

Implemented Bronze validation includes:

- Source schema validation
- Data-type validation
- Business-key NULL checks
- Business-grain uniqueness validation
- ETL control status tracking
- Source-file hashing
- Error capture in the control table

Silver and Gold validation responsibilities are defined in the architecture but remain pending implementation.

---

# Data Lineage

~~~text
CSV
 │
 ▼
BRONZE_POLICY_DATA
 │
 ▼
Silver subject-area tables
 │
 ▼
Gold dimensions / facts
 │
 ├────────► Planned FastAPI
 ├────────► Planned Streamlit
 ├────────► Planned RAG
 └────────► Planned NL2SQL
~~~

Complete source-record lineage is preserved through the implemented Bronze layer and is planned to be propagated into Silver and Gold.

---

# Frozen Design Decisions

| Decision | Value |
|----------|-------|
| Source | CSV Dataset |
| ETL Engine | PySpark |
| Database | Oracle 21c XE |
| Architecture | Medallion |
| Bronze Incremental Strategy | SOURCE_FILE + SHA-256 |
| Bronze Write Strategy | APPEND |
| Silver Incremental Strategy | MERGE / UPSERT — planned |
| Silver MERGE Key | (ID_POLICY, ID_INSURED, PERIOD) |
| Workflow Orchestration | Apache Airflow — planned |
| API Layer | FastAPI — planned |
| Dashboard | Streamlit — planned |
| AI Layer | RAG + NL2SQL — planned |

---

# Implementation Status

| Component | Status |
|-----------|--------|
| Bronze ETL | Implemented and validated end-to-end |
| Silver logical model | Frozen |
| Silver DDL | Pending |
| Silver ETL | Pending |
| Gold model | Target architecture / pending implementation |
| Airflow | Planned |
| FastAPI | Planned |
| Streamlit | Planned |
| RAG | Planned |
| NL2SQL | Planned |
