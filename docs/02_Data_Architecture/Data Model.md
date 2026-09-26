# Data Model

## Purpose

This document describes the logical data model used throughout the Medallion Architecture.

The project follows a layered data model:

- Bronze stores the source dataset with required technical type conversions and full source lineage.
- Silver separates the data into business-oriented subject areas while preserving the business observation grain.
- Gold organizes the data into a dimensional model (Star Schema) for analytics and downstream applications.

The business observation grain is preserved through Bronze and Silver. Gold dimensions and facts have their own documented grains.

---

# Business Grain

The business observation grain is:

```
(ID_POLICY, ID_INSURED, PERIOD)
```

Where:

| Attribute | Description |
|----------|-------------|
| ID_POLICY | Insurance policy identifier |
| ID_INSURED | Insured individual identifier within the policy |
| PERIOD | Calendar year |

This composite business key identifies one insured individual under one policy during one observation year.

---

# Bronze Layer Data Model

## Table

```
BRONZE_POLICY_DATA
```

### Description

Stores the source dataset at Bronze layer grain with required technical type conversions and complete source-record lineage.

### Characteristics

- Single source table
- One row per source observation
- Source columns retained
- Technical date and numeric type conversions applied
- Record-level hash retained
- ETL audit columns retained
- File-level incremental detection using source filename + SHA-256
- Bronze persistence uses append

---

# Silver Layer Data Model

The Silver layer contains eight subject-oriented tables. Each table is a logical projection of the same observation-level business grain unless otherwise stated.

## SILVER_RECORD

Technical and record-level subject area.

Typical columns:

- ID
- ID_POLICY
- ID_INSURED
- PERIOD
- RECORD_HASH
- LOAD_ID
- LOAD_TIMESTAMP
- SOURCE_FILE
- ETL_CREATED_BY

---

## SILVER_TIME

Time-related attributes associated with the observation.

Typical columns:

- PERIOD
- YEAR_EFFECT_INSURED
- YEAR_LAPSE_INSURED
- YEAR_EFFECT_POLICY
- YEAR_LAPSE_POLICY

---

## SILVER_POLICY

Policy-related attributes at observation grain.

Typical columns:

- ID_POLICY
- ID_INSURED
- PERIOD
- DATE_EFFECT_POLICY
- DATE_LAPSE_POLICY
- SENIORITY_POLICY
- TYPE_POLICY
- TYPE_POLICY_DG
- NEW_BUSINESS
- LAPSE

---

## SILVER_CUSTOMER

Insured-person attributes at observation grain.

Typical columns:

- ID_INSURED
- ID_POLICY
- PERIOD
- DATE_EFFECT_INSURED
- DATE_LAPSE_INSURED
- SENIORITY_INSURED
- GENDER
- AGE

---

## SILVER_PRODUCT

Insurance product attributes at observation grain.

Typical columns:

- ID_POLICY
- ID_INSURED
- PERIOD
- TYPE_PRODUCT
- REIMBURSEMENT

---

## SILVER_CHANNEL

Distribution-channel attributes at observation grain.

Typical columns:

- ID_POLICY
- ID_INSURED
- PERIOD
- DISTRIBUTION_CHANNEL

---

## SILVER_COVERAGE

Coverage and utilization measures at observation grain.

Typical columns:

- ID_POLICY
- ID_INSURED
- PERIOD
- EXPOSURE_TIME
- N_MEDICAL_SERVICES

---

## SILVER_FINANCIAL

Policy financial measures at observation grain.

Typical columns:

- ID_POLICY
- ID_INSURED
- PERIOD
- PREMIUM
- COST_CLAIMS_YEAR

`COST_CLAIMS_YEAR` is retained as a financial measure; it does not imply a separate claim-level entity.

---

# Research Enrichment Attributes

The source dictionary identifies the following research-enrichment/contextual attributes as Bronze-only for the current Silver design:

- N_INSURED_PC
- N_INSURED_MUN
- N_INSURED_PROV
- IICIMUN
- IICIPROV
- C_H
- C_GI
- C_II
- C_IE_P
- C_IE_S
- C_IE_T
- C_GE_P
- C_GE_S
- C_GE_T
- C_C

These attributes remain safely preserved in Bronze and are not forced into a Silver table without a stronger business-domain requirement.

---

# Silver Loading Strategy

Silver is planned to use Oracle MERGE/upsert processing at the frozen business observation grain:

```
(ID_POLICY, ID_INSURED, PERIOD)
```

Conceptually:

```
Bronze observation
      |
      v
Validate / standardize
      |
      v
Match Silver on (ID_POLICY, ID_INSURED, PERIOD)
      |
      +---- matched     -> UPDATE
      |
      +---- not matched -> INSERT
```

This is incremental current-state maintenance. It is **not SCD Type 2**.

A true SCD Type 2 implementation requires historical versions, effective/expiry dates or equivalent temporal attributes, and current-row handling. Such behavior will be evaluated for Gold dimensions where the business requirement justifies historical tracking.

---

# Gold Layer Data Model

The Gold layer follows a Star Schema.

## Dimension Tables

### DIM_POLICY

Stores policy attributes.

### DIM_CUSTOMER

Stores insured person attributes.

### DIM_PRODUCT

Stores insurance product information.

### DIM_CHANNEL

Stores distribution channel information.

### DIM_TIME

Stores calendar information.

## Fact Tables

### FACT_POLICY

Stores policy-level business measures.

### FACT_CLAIMS

The current Gold claims fact is retained as a future design decision. Silver does not introduce a separate claim entity because the source does not contain a separate claim-level business grain.

---

# Layer Relationships

```
                    BRONZE_POLICY_DATA
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
    Silver subject-area projections at
    (ID_POLICY, ID_INSURED, PERIOD)
          |
          +--> SILVER_RECORD
          +--> SILVER_TIME
          +--> SILVER_POLICY
          +--> SILVER_CUSTOMER
          +--> SILVER_PRODUCT
          +--> SILVER_CHANNEL
          +--> SILVER_COVERAGE
          +--> SILVER_FINANCIAL
                             |
                             v
                       PySpark Gold ETL
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
     Dimensions          Facts             Future SCD2
     / Star Schema       / Measures        where justified
```

---

# Data Model Principles

The data model follows these principles:

- Bronze preserves the source dataset and complete source-record lineage.
- Silver represents meaningful business/domain subject areas rather than leftover-column buckets.
- The frozen business observation grain is preserved in Silver.
- Silver uses planned Oracle MERGE/upsert processing at the business grain.
- MERGE/upsert is not treated as SCD Type 2.
- Gold follows dimensional modeling and may use SCD Type 2 where a business requirement exists.
- Full lineage is maintained from Bronze to Gold.
- No separate Silver claims or enrichment entity is introduced without a justified business grain.

---

# Frozen Design Decisions

| Decision | Value |
|----------|-------|
| Architecture | Medallion |
| Data Model | Star Schema |
| Business Observation Grain | (ID_POLICY, ID_INSURED, PERIOD) |
| Bronze Tables | 1 |
| Silver Tables | 8 |
| Gold Dimensions | 5 |
| Gold Facts | 2 |
| Bronze Incremental Detection | SOURCE_FILE + SHA-256 |
| Bronze Write Strategy | APPEND |
| Silver Write Strategy | MERGE / UPSERT |
| Silver MERGE Key | (ID_POLICY, ID_INSURED, PERIOD) |
| SCD Type 2 | Future Gold design decision where justified |
| ETL Engine | PySpark |
| Database | Oracle 21c XE |

---

# Model Summary

| Layer | Purpose |
|--------|---------|
| Bronze | Source preservation, technical type conversion, lineage and file-level incremental ingestion |
| Silver | Validated, standardized, subject-oriented projections at business observation grain |
| Gold | Dimensional model for analytics and downstream applications |

---

# Implementation Status

The Bronze layer is implemented and has been validated end-to-end against the original dataset.

The eight-table Silver model is frozen logically, but Silver DDL and ETL implementation are still pending.
