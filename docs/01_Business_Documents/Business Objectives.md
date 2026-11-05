# Business Objectives

## Project Name

Insurance Risk Intelligence Platform

## Purpose

Build an insurance data engineering and analytics platform that demonstrates data warehousing, ETL, dimensional modelling, orchestration, API development and interactive analytics. GenAI/RAG capabilities remain a future phase.

## Business Problem

The project uses an insurance research dataset to organize policy, insured, product, channel, coverage and financial observations into a warehouse that can support portfolio analysis. The current implementation provides a curated Oracle star schema, read-only analytics API and Streamlit dashboard.

The source and implemented model do not establish a separate claim-level business entity. Annual claim cost is represented as a measure at the policy-insured-period observation grain.

## Objectives and implementation status

| Objective | Current status evidenced by repository |
|---|---|
| Design an Insurance Data Warehouse using Medallion Architecture | Implemented: Bronze, Silver and Gold |
| Build ETL pipelines using PySpark | Implemented for Bronze, Silver and Gold |
| Store curated data in Oracle | Implemented |
| Apply dimensional modelling | Implemented: five dimensions and FACT_POLICY |
| Validate data quality and warehouse reconciliation | Implemented; execution evidence in `docs/VALIDATION.md` |
| Orchestrate ETL workflows | Implemented in Python orchestration and an Airflow DAG; DAG is manually triggered/unscheduled |
| Expose analytics through REST APIs | Implemented using FastAPI; see API source and README |
| Provide interactive analytics | Implemented using Streamlit; see `docs/DASHBOARD.md` |
| Enable RAG-based business-document retrieval | Future phase; not implemented |
| Enable NL2SQL / natural-language querying | Future phase; not implemented |
| Add an LLM provider, embedding model or vector database | Not selected/implemented in the current repository |
| Maintain metadata and lineage | Technical lineage fields are implemented in the warehouse; broader governance capabilities should not be inferred |

## Scope

### Implemented scope

- CSV ingestion and Bronze persistence.
- Silver subject projections and Oracle MERGE.
- Gold star-schema construction and full-refresh loading.
- Data quality validation and Bronze/Silver/Gold reconciliation.
- Python and Airflow orchestration.
- Read-only FastAPI analytics service.
- Streamlit dashboard consuming the API.

### Future scope

- RAG over approved business and technical documentation.
- LLM integration and provider selection.
- Embedding generation and vector database.
- NL2SQL, subject to controlled query design and validation.

### Not evidenced as implemented

The current repository does not establish real-time streaming, CDC ingestion, production cloud deployment, production scheduling, CI/CD, multi-user management, or an implemented RAG/NL2SQL assistant. Do not represent these as delivered capabilities.

## Expected analytical use

The implemented dashboard/API exposes portfolio, yearly, product, channel, policy, customer and customer-cohort analyses. The exact metrics and grain must follow the API queries and dashboard metric definitions; this document does not add new KPI formulas or business rules.

## Technology stack

| Area | Implemented technology / status |
|---|---|
| Data processing | Python, PySpark |
| Warehouse database | Oracle |
| Orchestration | Python orchestration and Apache Airflow DAG (manual/unscheduled) |
| Analytics API | FastAPI |
| Dashboard | Streamlit |
| GenAI / RAG / NL2SQL | Future phase; provider, framework, embeddings and vector store not frozen |

## Related implementation documentation

- `docs/ARCHITECTURE.md`
- `docs/02_Data_Architecture/Data Model.md`
- `docs/02_Data_Architecture/Data Flow.md`
- `docs/ORCHESTRATION.md`
- `docs/DASHBOARD.md`
- `docs/VALIDATION.md`
