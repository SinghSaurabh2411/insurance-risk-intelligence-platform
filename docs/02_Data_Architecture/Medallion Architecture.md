# Medallion Architecture

## Purpose

This project follows the **Medallion Architecture** to organize data into progressive quality layers.

Each layer has a clearly defined responsibility:

- **Bronze** stores the raw source dataset.
- **Silver** stores cleaned, standardized, and business-oriented data.
- **Gold** stores dimensional models and fact tables optimized for analytics, APIs, dashboards, and AI applications.

This layered approach improves maintainability, data quality, traceability, and scalability while keeping ETL logic modular.

---

# Architecture Overview

```
                    Source Dataset (CSV)
                            │
                            │
                    PySpark Bronze ETL
                            │
                            ▼
                 BRONZE_POLICY_DATA
                            │
                            │
                    PySpark Silver ETL
                            │
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼              ▼
 SILVER_POLICY  SILVER_CUSTOMER SILVER_PRODUCT SILVER_CLAIMS SILVER_ENRICHMENT
      │              │              │              │              │
      └──────────────┴──────────────┴──────────────┴──────────────┘
                            │
                    PySpark Gold ETL
                            │
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
 DIM_POLICY     DIM_CUSTOMER   DIM_PRODUCT   DIM_CHANNEL
      │
      ├──────────────┐
      ▼              ▼
 DIM_TIME      FACT_POLICY

                     FACT_CLAIMS
```

---

# Bronze Layer

## Purpose

The Bronze layer stores the raw dataset exactly as received from the source system.

No business rules are applied except basic datatype conversion required for Oracle compatibility.

The Bronze layer acts as the immutable source for all downstream processing.

### Characteristics

- Raw source data
- One table
- Minimal transformation
- Full data lineage preserved
- Source values retained
- Supports incremental MERGE loads

### Table

| Table |
|---------|
| BRONZE_POLICY_DATA |

---

# Silver Layer

## Purpose

The Silver layer contains cleansed, validated, and logically separated business entities.

Data is standardized into subject-oriented tables to reduce redundancy and simplify downstream processing.

### Transformations

- Data validation
- Null handling
- Date standardization
- Data type conversion
- Business rule validation
- Entity separation
- Duplicate handling
- Incremental MERGE

### Tables

| Table | Purpose |
|---------|----------|
| SILVER_POLICY | Policy-related attributes |
| SILVER_CUSTOMER | Customer attributes |
| SILVER_PRODUCT | Product information |
| SILVER_CLAIMS | Claims summary |
| SILVER_ENRICHMENT | Socioeconomic & environmental enrichment |

---

# Gold Layer

## Purpose

The Gold layer provides analytics-ready dimensional models.

This layer follows a Star Schema consisting of dimensions and fact tables.

The Gold layer is optimized for:

- BI Dashboards
- KPI Reporting
- FastAPI
- Streamlit
- RAG
- NL2SQL

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
| FACT_CLAIMS | Claims metrics |

---

# Incremental Loading Strategy

Although the source dataset is static, the ETL pipeline is designed as if new data arrives periodically.

This simulates a production-grade Data Engineering workflow.

The pipeline performs incremental loading using Oracle `MERGE` statements.

### Business Grain

```
(ID_POLICY,
 ID_INSURED,
 PERIOD)
```

This composite business key uniquely identifies each record during ETL processing.

### Benefits

- Prevents duplicate records
- Supports updates
- Supports late-arriving records
- Simulates production ETL design
- Enables future scalability

---

# Data Quality Responsibilities

| Layer | Responsibility |
|---------|----------------|
| Bronze | Preserve raw source data |
| Silver | Clean, validate and standardize |
| Gold | Analytics-ready dimensional model |

---

# Design Principles

The Medallion Architecture in this project follows these principles:

- Raw data is never modified.
- Every transformation is traceable.
- Business entities are separated in the Silver layer.
- Gold follows dimensional modeling.
- Incremental loading is implemented using Oracle MERGE.
- Business grain remains fixed throughout the pipeline.
- Data lineage is preserved from Bronze to Gold.

---

# Frozen Design Decisions

| Decision | Status |
|-----------|--------|
| Architecture | Medallion |
| ETL Engine | PySpark |
| Database | Oracle 21c XE |
| Incremental Loading | MERGE |
| Business Grain | (ID_POLICY, ID_INSURED, PERIOD) |
| Bronze Table | BRONZE_POLICY_DATA |
| Silver Layer | Subject-oriented tables |
| Gold Layer | Star Schema |
| Source Dataset | Static CSV |