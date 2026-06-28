# Naming Conventions

## Purpose

This document defines the naming standards used throughout the project.

The objective is to maintain consistency, readability, and scalability across the data warehouse, ETL pipelines, APIs, and supporting components.

These conventions apply to all current and future project artifacts.

---

# General Principles

- Use uppercase for all Oracle database objects.
- Use snake_case for Python files and variables.
- Use meaningful business names.
- Avoid abbreviations unless they are standard business terms.
- Keep names consistent across all layers.
- Follow the same naming convention for future objects.

---

# Database Object Naming

## Bronze Tables

Pattern

```
BRONZE_<ENTITY_NAME>
```

Examples

```
BRONZE_POLICY_DATA
BRONZE_CUSTOMER_DATA
```

---

## Silver Tables

Pattern

```
SILVER_<ENTITY_NAME>
```

Examples

```
SILVER_POLICY
SILVER_CUSTOMER
SILVER_PRODUCT
SILVER_CLAIMS
SILVER_ENRICHMENT
```

---

## Gold Dimension Tables

Pattern

```
DIM_<ENTITY_NAME>
```

Examples

```
DIM_POLICY
DIM_CUSTOMER
DIM_PRODUCT
DIM_CHANNEL
DIM_TIME
```

---

## Gold Fact Tables

Pattern

```
FACT_<BUSINESS_PROCESS>
```

Examples

```
FACT_POLICY
FACT_CLAIMS
```

---

## Views

Pattern

```
VW_<NAME>
```

Example

```
VW_POLICY_SUMMARY
```

---

## Materialized Views

Pattern

```
MV_<NAME>
```

Example

```
MV_POLICY_KPI
```

---

# Column Naming

Columns use uppercase with underscores.

Pattern

```
COLUMN_NAME
```

Examples

```
ID_POLICY
ID_INSURED
PERIOD
PREMIUM
AGE
DATE_EFFECT_POLICY
```

---

# Primary Keys

Pattern

```
PK_<TABLE_NAME>
```

Examples

```
PK_DIM_POLICY

PK_FACT_POLICY
```

---

# Foreign Keys

Pattern

```
FK_<CHILD_TABLE>_<PARENT_TABLE>
```

Examples

```
FK_FACT_POLICY_DIM_POLICY

FK_FACT_POLICY_DIM_CUSTOMER
```

---

# Indexes

Pattern

```
IDX_<TABLE_NAME>_<COLUMN_NAME>
```

Examples

```
IDX_DIM_POLICY_ID_POLICY

IDX_FACT_POLICY_PERIOD
```

---

# Sequences

Pattern

```
SEQ_<TABLE_NAME>
```

Example

```
SEQ_DIM_CUSTOMER
```

---

# Constraints

Pattern

```
CK_<TABLE_NAME>_<COLUMN_NAME>
```

Example

```
CK_DIM_CUSTOMER_GENDER
```

---

# ETL Script Naming

Python ETL scripts follow:

```
<layer>_<entity>_etl.py
```

Examples

```
bronze_ingestion_etl.py

silver_policy_etl.py

silver_customer_etl.py

gold_policy_etl.py
```

---

# Utility Scripts

Pattern

```
<purpose>.py
```

Examples

```
config.py

logger.py

jdbc_connection.py

merge_loader.py

validation.py
```

---

# Airflow DAG Naming

Pattern

```
<layer>_<process>_dag.py
```

Examples

```
bronze_etl_dag.py

silver_etl_dag.py

gold_etl_dag.py

daily_pipeline_dag.py
```

---

# API Naming

REST endpoints follow plural resource naming.

Pattern

```
/api/v1/<resource>
```

Examples

```
/api/v1/policies

/api/v1/customers

/api/v1/claims
```

---

# Streamlit Pages

Pattern

```
<page_name>.py
```

Examples

```
dashboard.py

policy_analysis.py

claims_analysis.py
```

---

# Git Branch Naming

Pattern

```
feature/<feature_name>

bugfix/<issue_name>

docs/<document_name>

release/<version>
```

Examples

```
feature/gold-layer

feature/airflow

docs/data-dictionary

bugfix/jdbc-connection
```

---

# Git Commit Convention

Pattern

```
<type>: <description>
```

Types

```
feat

fix

docs

refactor

test

chore
```

Examples

```
feat: implement bronze ingestion

feat: create silver policy ETl

docs: update business glossary

fix: jdbc connection issue
```

---

# Logging Convention

Format

```
[Timestamp] [Layer] [Status] Message
```

Example

```
2026-07-01 10:15:12

[BRONZE]

[SUCCESS]

Loaded 125,456 records
```

---

# Future Objects

Any future database object introduced into the project should follow the conventions defined in this document.

This ensures consistency as the warehouse evolves.

---

# Frozen Standards

| Object | Convention |
|----------|------------|
| Bronze Tables | BRONZE_* |
| Silver Tables | SILVER_* |
| Dimension Tables | DIM_* |
| Fact Tables | FACT_* |
| Views | VW_* |
| Materialized Views | MV_* |
| Primary Keys | PK_* |
| Foreign Keys | FK_* |
| Indexes | IDX_* |
| Sequences | SEQ_* |
| Constraints | CK_* |
| ETL Scripts | layer_entity_etl.py |
| Airflow DAGs | layer_process_dag.py |
| REST APIs | /api/v1/resource |
| Python Variables | snake_case |
| Oracle Objects | UPPERCASE |

---

# Summary

This naming convention provides a consistent standard for database objects, ETL components, APIs, orchestration workflows, and supporting project artifacts. The conventions are designed to support future expansion while maintaining readability and consistency across the entire data engineering solution.