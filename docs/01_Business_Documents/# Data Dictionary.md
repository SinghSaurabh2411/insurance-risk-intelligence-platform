# Data Dictionary

## Version

| Item | Value |
|------|------|
| Version | 1.0 |
| Status | Frozen |
| Last Updated | 28-Jun-2026 |
| Author | Saurabh Singh |

---

# Purpose

This document defines the metadata for the Insurance Policy Data Warehouse.

It provides:

- Business meaning of every source attribute
- Data type mappings
- Bronze, Silver and Gold layer lineage
- Data quality expectations
- Transformation requirements
- Usage within reporting, analytics and AI workloads

This document should be considered the single source of truth for all data engineering and analytics development.

---

# Data Warehouse Layers

| Layer | Purpose |
|---------|----------|
| Bronze | Raw source data ingested with minimal changes |
| Silver | Cleansed, standardized and business-oriented tables |
| Gold | Dimensional model (Dimensions and Facts) used for reporting, analytics and machine learning |

---

# Column Definitions

| Column | Description |
|---------|-------------|
| Variables | Source attribute name |
| Description | Original business description |
| Expanded Description | Detailed business definition |
| Business Domain | Functional business area |
| Business Entity | Logical entity |
| Source Data Type | Original datatype |
| Oracle Data Type | Oracle implementation |
| Source Category | Indicates whether the field originates from the source system or research enrichment |
| Bronze Layer Table | Landing table |
| Silver Layer Table | Curated table |
| Gold Layer Object | Target Dimension/Fact |
| Transformation Required | Indicates whether ETL transformation is required |
| Nullable | Whether NULL values are permitted |
| Primary Key | Indicates PK participation |
| Foreign Key | Indicates FK participation |
| Data Quality Rule | Validation rule |
| Used In | Downstream consumers |
| Remarks | Additional implementation notes |

---

# Data Dictionary

> **Note**
>
> Due to the width of the metadata, the complete Data Dictionary is maintained in the accompanying Excel workbook (`Data_Dictionary.xlsx`).
>
> This Markdown document serves as the functional documentation, while the Excel workbook remains the authoritative metadata repository.

The Excel workbook contains metadata for the following domains:

- Technical
- Customer
- Policy
- Product
- Claims
- Sales
- Time
- Socioeconomic Enrichment
- Environmental Enrichment

including:

- 40+ business attributes
- Complete Oracle datatype mapping
- Bronze → Silver → Gold lineage
- Data quality rules
- Transformation requirements
- Nullable constraints
- Key definitions
- Business usage

---

# Naming Standards

## Bronze Tables

```
BRONZE_POLICY_DATA
```

---

## Silver Tables

```
SILVER_CUSTOMER
SILVER_POLICY
SILVER_PRODUCT
SILVER_CLAIMS
SILVER_ENRICHMENT
```

---

## Gold Objects

### Dimensions

```
DIM_CUSTOMER
DIM_POLICY
DIM_PRODUCT
DIM_CHANNEL
DIM_TIME
```

### Facts

```
FACT_POLICY
FACT_CLAIMS
```

---

# Data Quality Standards

The following validations apply across the warehouse.

| Category | Rule |
|-----------|------|
| IDs | Must be unique where applicable |
| Dates | Valid Oracle DATE values |
| Numeric values | Must be within defined business ranges |
| Nullable fields | Only fields explicitly marked Nullable = Yes may contain NULL |
| Enumerations | Must conform to documented source values |
| Keys | Business keys preserved from source |

---

# Transformation Standards

General ETL principles:

- Preserve source business keys.
- Standardize Oracle datatypes.
- Convert source dates to Oracle DATE.
- Preserve research enrichment fields where applicable.
- Remove redundant attributes from Gold unless required for reporting or AI.
- Maintain end-to-end lineage from Bronze to Gold.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 28-Jun-2026 | Initial frozen version |