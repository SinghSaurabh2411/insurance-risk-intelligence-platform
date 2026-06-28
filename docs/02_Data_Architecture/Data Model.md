# Data Model

## Purpose

This document describes the logical data model used throughout the Medallion Architecture.

The project follows a layered data model:

- Bronze stores the raw source dataset.
- Silver separates the data into business entities.
- Gold organizes the data into a dimensional model (Star Schema) for analytics and downstream applications.

The business grain is preserved throughout the pipeline.

---

# Business Grain

The business grain is defined as:

```
(ID_POLICY, ID_INSURED, PERIOD)
```

Where:

| Attribute | Description |
|----------|-------------|
| ID_POLICY | Insurance policy identifier |
| ID_INSURED | Insured individual identifier within the policy |
| PERIOD | Calendar year |

This composite business key uniquely identifies one insured individual under one policy during one observation year.

The same grain is maintained across the Bronze, Silver, and Gold layers.

---

# Bronze Layer Data Model

## Table

```
BRONZE_POLICY_DATA
```

### Description

Stores the raw source dataset with minimal transformation.

### Characteristics

- Single source table
- One row per business grain
- Full source lineage retained
- Source values preserved
- Supports incremental MERGE loading

---

# Silver Layer Data Model

The Silver layer separates the Bronze dataset into business-oriented entities.

## SILVER_POLICY

Contains policy-related information.

### Examples

- ID_POLICY
- PERIOD
- POLICY DATES
- POLICY TYPE
- PREMIUM
- EXPOSURE
- LAPSE
- NEW BUSINESS

---

## SILVER_CUSTOMER

Contains insured person attributes.

### Examples

- ID_POLICY
- ID_INSURED
- PERIOD
- AGE
- GENDER
- SENIORITY
- INSURED DATES

---

## SILVER_PRODUCT

Contains insurance product information.

### Examples

- PRODUCT TYPE
- REIMBURSEMENT

---

## SILVER_CLAIMS

Contains yearly claims information.

### Examples

- COST_CLAIMS_YEAR
- N_MEDICAL_SERVICES

---

## SILVER_ENRICHMENT

Contains external enrichment attributes.

### Examples

- HABITAT CATEGORY
- INCOME CATEGORY
- CLIMATE CATEGORY

---

# Gold Layer Data Model

The Gold layer follows a Star Schema.

## Dimension Tables

### DIM_POLICY

Stores policy attributes.

---

### DIM_CUSTOMER

Stores insured person attributes.

---

### DIM_PRODUCT

Stores insurance product information.

---

### DIM_CHANNEL

Stores distribution channel information.

---

### DIM_TIME

Stores calendar information.

---

## Fact Tables

### FACT_POLICY

Stores policy-level business measures.

Typical measures include:

- Premium
- Exposure Time
- New Business
- Lapse Status

---

### FACT_CLAIMS

Stores yearly healthcare utilization measures.

Typical measures include:

- Claims Cost
- Medical Services Count

---

# Layer Relationships

```
                    BRONZE_POLICY_DATA
                             │
               ──────────────┼──────────────
                             │
      ┌──────────────┬───────────────┬──────────────┬────────────┐
      ▼              ▼               ▼              ▼            ▼
SILVER_POLICY SILVER_CUSTOMER SILVER_PRODUCT SILVER_CLAIMS SILVER_ENRICHMENT
      │              │               │             │             │
      └──────────────┴───────────────┴─────────────┴─────────────┘
                             │
                ─────────────┼─────────────
                             │
      ┌────────────┬────────────┬────────────┬─────────────┐
      ▼            ▼            ▼            ▼             ▼
 DIM_POLICY  DIM_CUSTOMER   DIM_PRODUCT   DIM_CHANNEL   DIM_TIME
      │
      ├─────────────────────────────┐
      ▼                             ▼
FACT_POLICY                 FACT_CLAIMS
```

---

# Dimensional Model

The Gold layer follows a Star Schema.

```
                 DIM_POLICY
                      │
                      │
DIM_CUSTOMER ── FACT_POLICY ── DIM_PRODUCT
                      │
                 DIM_CHANNEL
                      │
                  DIM_TIME


                 DIM_CUSTOMER
                      │
                      │
                 FACT_CLAIMS
                      │
                  DIM_TIME
```

---

# Data Model Principles

The data model follows these principles:

- One source of truth in the Bronze layer.
- Business entities separated in the Silver layer.
- Analytics-ready Star Schema in the Gold layer.
- Business grain preserved across all layers.
- Incremental processing implemented using Oracle MERGE.
- Full lineage maintained from Bronze to Gold.
- Subject-oriented design minimizes data redundancy.

---

# Frozen Design Decisions

| Decision | Value |
|----------|-------|
| Architecture | Medallion |
| Data Model | Star Schema |
| Business Grain | (ID_POLICY, ID_INSURED, PERIOD) |
| Bronze Tables | 1 |
| Silver Tables | 5 |
| Gold Dimensions | 5 |
| Gold Facts | 2 |
| Incremental Strategy | MERGE |
| ETL Engine | PySpark |
| Database | Oracle 21c XE |

---

# Model Summary

| Layer | Purpose |
|--------|---------|
| Bronze | Raw source data |
| Silver | Cleansed business entities |
| Gold | Dimensional model for analytics |