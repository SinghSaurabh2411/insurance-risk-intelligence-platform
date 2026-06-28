# Data Flow

## Purpose

This document describes the end-to-end movement of data through the platform.

The project follows a Medallion Architecture where data progresses through Bronze, Silver, and Gold layers before being consumed by downstream applications.

The ETL pipeline is implemented using PySpark and orchestrated using Apache Airflow.

---

# End-to-End Data Flow

```
                                  Source Dataset (CSV)
                                          │
                                          │
                                          ▼
                                  PySpark Bronze ETL
                                          │
                                          ▼
                                  BRONZE_POLICY_DATA
                                          │
                                          │
                                  PySpark Silver ETL
                                          │
      ┌────────────────┬──────────────────┬──────────────┬──────────────────┐
      ▼                ▼                  ▼              ▼                  ▼
SILVER_POLICY    SILVER_CUSTOMER    SILVER_PRODUCT   SILVER_CLAIMS    SILVER_ENRICHMENT

                                          │
                            ──────────────┼──────────────
                                          │
                                   PySpark Gold ETL
                                          │
                  ┌──────────────┬──────────────┬──────────────┬──────────────┐
                  ▼              ▼              ▼              ▼              ▼
            DIM_POLICY   DIM_CUSTOMER      DIM_PRODUCT   DIM_CHANNEL     DIM_TIME
                                          │
                                  ┌───────┴────────┐
                                  ▼                ▼
                              FACT_POLICY      FACT_CLAIMS
                              
                                          │
                                 ─────────┼─────────
                                          │
                             ┌────────────┼────────────┐
                             ▼            ▼            ▼
                          FastAPI      Streamlit    RAG / NL2SQL
```

---

# Data Processing Flow

The ETL pipeline processes the data through three logical layers.

```
Source CSV
      │
      ▼
Bronze Layer
      │
      ▼
Silver Layer
      │
      ▼
Gold Layer
      │
      ▼
Analytics & AI Applications
```

---

# Step 1 – Source Ingestion

Input consists of a structured CSV dataset containing insurance policy information.

The source dataset is treated as the authoritative source of truth.

Although the dataset is static, the ETL pipeline is designed to support incremental processing using Oracle MERGE statements.

---

# Step 2 – Bronze Layer

The Bronze ETL performs:

- CSV ingestion
- Schema validation
- Data type conversion
- Basic data quality validation
- Oracle loading into BRONZE_POLICY_DATA

No business transformations are performed.

Purpose:

- Preserve source data
- Maintain lineage
- Provide a recoverable raw layer

---

# Step 3 – Silver Layer

The Silver ETL reads the Bronze table and separates the data into business entities.

Business entities include:

- Policy
- Customer
- Product
- Claims
- Enrichment

Typical transformations include:

- Data validation
- Null handling
- Standardization
- Entity separation
- Duplicate removal
- Business rule validation
- Incremental MERGE loading

---

# Step 4 – Gold Layer

The Gold ETL builds a dimensional model.

Dimension tables store descriptive business attributes.

Fact tables store measurable business metrics.

The Gold layer is optimized for analytical workloads.

---

# Incremental Processing

Although the dataset is static, the ETL pipeline is implemented as an incremental process to simulate a production-grade data engineering solution.

Incremental loading uses Oracle MERGE statements.

Business grain:

```
(ID_POLICY,
 ID_INSURED,
 PERIOD)
```

For every ETL execution:

- Existing records are updated.
- New records are inserted.
- Duplicate records are prevented.

---

# Data Consumption

The Gold layer serves as the single source for downstream applications.

## FastAPI

Provides REST APIs for accessing dimensional and fact data.

---

## Streamlit

Provides interactive dashboards for business users.

---

## RAG

Retrieves business metadata and documentation to answer natural language questions.

---

## NL2SQL

Converts natural language queries into SQL statements executed against the Gold schema.

---

# Workflow Orchestration

Apache Airflow orchestrates the ETL workflow.

Pipeline execution order:

```
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

API Refresh

↓

Dashboard Refresh
```

---

# Error Handling

At each layer, the pipeline performs validation before continuing.

Validation includes:

- Schema validation
- Data type validation
- Mandatory field validation
- Duplicate detection
- Business rule validation

Records failing validation are logged for investigation.

---

# Data Lineage

```
CSV
 │
 ▼
BRONZE_POLICY_DATA
 │
 ▼
Silver Tables
 │
 ▼
Gold Tables
 │
 ├────────► FastAPI
 │
 ├────────► Streamlit
 │
 ├────────► RAG
 │
 └────────► NL2SQL
```

Every record can be traced from the Gold layer back to the original source dataset.

---

# Frozen Design Decisions

| Decision | Value |
|----------|-------|
| Source | CSV Dataset |
| ETL Engine | PySpark |
| Database | Oracle 21c XE |
| Architecture | Medallion |
| Incremental Strategy | MERGE |
| Business Grain | (ID_POLICY, ID_INSURED, PERIOD) |
| Workflow Orchestration | Apache Airflow |
| API Layer | FastAPI |
| Dashboard | Streamlit |
| AI Layer | RAG + NL2SQL |

---

# Summary

The data flow follows a structured Medallion Architecture in which raw data is ingested into the Bronze layer, transformed into business-oriented Silver tables, and modeled into Gold dimensional tables.

The Gold layer acts as the single source of truth for analytics, dashboards, APIs, and AI-powered services while preserving full lineage back to the original source dataset.