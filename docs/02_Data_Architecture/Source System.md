# Source System

**Version:** 2.0
**Status:** 🔒 Frozen
**Owner:** Data Engineering Team

---

# 1. Purpose

This document describes the source system used in the Insurance Lakehouse project. It defines the characteristics of the source dataset, ingestion strategy, record grain, business keys, and architectural assumptions that govern data ingestion into the Medallion Architecture.

Although the source dataset is static, the ingestion framework is intentionally designed using production-grade incremental loading patterns to simulate a real-world enterprise data platform.

---

# 2. Source Overview

| Attribute             | Value                         |
| --------------------- | ----------------------------- |
| Source Type           | Structured Dataset            |
| Domain                | Health Insurance              |
| Source Format         | Microsoft Excel (.xlsx)       |
| Source System         | Research Dataset              |
| Ingestion Type        | Batch                         |
| Pipeline Design       | Incremental Batch Processing  |
| Initial Load          | Full Load                     |
| Ongoing Load Strategy | Incremental MERGE             |
| Refresh Frequency     | Simulated Periodic Batch Load |
| Data Volume           | ~220,000+ Records             |
| Number of Attributes  | 42                            |
| Observation Period    | Multiple Calendar Years       |
| Primary Language      | English                       |

---

# 3. Dataset Description

The dataset contains insurance policy information for individual insured members across multiple calendar years.

Each record combines customer information, policy attributes, insurance products, claims utilization, and selected socioeconomic enrichment variables.

The dataset is treated as the operational source for the Lakehouse implementation.

---

# 4. Business Grain (Frozen)

Each record represents exactly one insured individual under one policy during one calendar year.

**Business Grain**

```text
(ID_policy, ID_insured, period)
```

Where:

* **ID_policy** → Insurance policy identifier
* **ID_insured** → Insured member within the policy
* **period** → Calendar year

This grain is maintained consistently throughout the Bronze, Silver, and Gold layers.

---

# 5. Business Keys

## Natural Business Key

```text
(ID_policy, ID_insured, period)
```

This composite key uniquely identifies every business record.

---

## Source Identifier

The dataset also provides:

```text
ID = ID_policy + ID_insured
```

The `ID` column is retained for lineage and traceability.

Since an insured individual may exist across multiple years, **`ID` alone is not sufficient to uniquely identify a record across the complete dataset**. Therefore, `period` forms part of the business grain.

---

# 6. Source Categories

The dataset contains two categories of data.

## Original Dataset

Business-operational insurance information including:

* Customer
* Policy
* Product
* Claims
* Premium
* Distribution Channel
* Policy Lifecycle

---

## Research Enrichment

Externally derived analytical attributes including:

* Income Segmentation
* Education Segmentation
* Habitat Classification
* Climate Classification
* Insurance Penetration Metrics

These attributes are selectively propagated beyond the Bronze layer based on analytical requirements.

---

# 7. Business Domains

The source dataset contains the following domains.

| Domain        | Description           |
| ------------- | --------------------- |
| Technical     | Record identifiers    |
| Customer      | Insured information   |
| Policy        | Policy lifecycle      |
| Product       | Insurance products    |
| Claims        | Medical utilization   |
| Sales         | Distribution channel  |
| Time          | Calendar information  |
| Socioeconomic | External enrichment   |
| Environmental | Geographic enrichment |

---

# 8. Source-to-Bronze Mapping

The complete source dataset is ingested into a single Bronze table.

| Source                    | Bronze Table       |
| ------------------------- | ------------------ |
| Insurance Dataset (.xlsx) | BRONZE_POLICY_DATA |

Bronze preserves the raw source with minimal transformation.

---

# 9. Source Data Characteristics

* Structured tabular dataset
* Mixed data types
* One record per business grain
* Nullable business attributes
* Historical yearly observations
* Includes research enrichment variables
* Suitable for incremental processing

---

# 10. Ingestion Strategy

Although the research dataset is delivered as a static Excel file, the ingestion framework is intentionally implemented using an incremental loading strategy to emulate a production insurance data platform.

The first execution performs a complete load.

Subsequent executions use Delta Lake `MERGE` operations to perform incremental upserts.

This enables:

* Idempotent pipeline execution
* Duplicate prevention
* Efficient reprocessing
* Slowly Changing Dimension (SCD) support
* Production-ready ETL design

---

# 11. Incremental Processing Strategy

| Attribute          | Value                           |
| ------------------ | ------------------------------- |
| Initial Load       | Full Load                       |
| Incremental Load   | Supported                       |
| Processing Pattern | Batch Incremental               |
| Merge Strategy     | Delta Lake MERGE                |
| Business Key       | (ID_policy, ID_insured, period) |
| Duplicate Handling | Upsert using MERGE              |
| Change Detection   | Business Key Comparison         |
| Pipeline Type      | Idempotent                      |

---

# 12. Data Quality Expectations

The source dataset is expected to satisfy the following conditions before Silver processing.

* Business grain must remain unique.
* Mandatory business keys cannot be null.
* Dates must be valid.
* Numeric fields must satisfy business rules defined in the Data Dictionary.
* Categorical values must conform to documented domains.

Any violations are handled within the Data Quality Framework during Silver processing.

---

# 13. Source Assumptions

The following assumptions apply throughout the project.

* The source dataset represents the system of record.
* Bronze stores the raw source with minimal transformation.
* Business transformations begin in the Silver layer.
* Missing lapse dates indicate active coverage.
* Research enrichment variables are informational and may not be promoted to downstream analytical models.
* Incremental loading is implemented as an architectural design decision despite the static nature of the dataset.

---

# 14. Source Limitations

* Dataset is a historical research dataset.
* No native Change Data Capture (CDC) is available.
* No streaming ingestion.
* Personally identifiable information has been anonymized.
* Research enrichment variables are precomputed statistics rather than operational source data.

---

# 15. Downstream Usage

The Bronze table is the source for the following Silver tables:

* SILVER_CUSTOMER
* SILVER_POLICY
* SILVER_PRODUCT
* SILVER_CLAIMS
* SILVER_ENRICHMENT

These curated datasets are used to build Gold dimension and fact tables for reporting, analytics, and machine learning.

---

# 16. Related Documents

* Business_Objective.md
* Business_Glossary.md
* Data_Dictionary.md
* Medallion_Architecture.md
* Data_Model.md
* ETL_Pipeline.md

---

# 17. Architecture Decisions (Frozen)

| Decision                                         | Status    |
| ------------------------------------------------ | --------- |
| Business Grain = (ID_policy, ID_insured, period) | 🔒 Frozen |
| Bronze Layer stores raw source                   | 🔒 Frozen |
| Silver Layer uses Delta MERGE                    | 🔒 Frozen |
| Gold Layer uses Delta MERGE                      | 🔒 Frozen |
| Incremental Batch Processing                     | 🔒 Frozen |
| Idempotent Pipeline Design                       | 🔒 Frozen |
| SCD support through MERGE operations             | 🔒 Frozen |
