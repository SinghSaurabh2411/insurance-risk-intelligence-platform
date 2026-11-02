# Insurance Risk Intelligence Platform

An end-to-end insurance data engineering and analytics platform built with Python, PySpark, Oracle, Apache Airflow, FastAPI, and Streamlit.

## Project status

The warehouse, orchestration, API, and interactive dashboard are implemented. The Bronze, Silver, and Gold layers remain frozen and are not to be redesigned without an explicit requirement.

| Component | Status |
|---|---|
| Bronze ingestion | Implemented and execution validated |
| Silver transformation | Implemented; DQ, reconciliation, and rerun validated |
| Gold dimensional warehouse | Implemented; grain, DQ, FK, and measure reconciliation validated |
| Pipeline orchestration | Implemented with fail-fast stage sequencing |
| Apache Airflow | DAG manually runtime-validated; intentionally unscheduled |
| FastAPI | Read-only, API-key-protected Gold analytics API |
| Streamlit | Six-page interactive analytics dashboard implemented |
| GenAI / RAG | Future phase |

## Architecture

```text
Source CSV
   |
   v
Bronze (Oracle)
   |
   v
Silver (Oracle)
   |
   v
Gold Star Schema (Oracle)
   |
   v
FastAPI (read-only analytics API)
   |
   v
Streamlit Dashboard
   |
   v
Future GenAI / RAG capabilities
```

The business grain throughout the warehouse is:

```text
(ID_POLICY, ID_INSURED, PERIOD)
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the frozen warehouse design and [docs/VALIDATION.md](docs/VALIDATION.md) for the recorded validation evidence.

## Data warehouse

### Bronze

- Oracle table: `DWH_BRONZE.BRONZE_POLICY_DATA`
- File-level SHA-256 detection and append loading.
- `RECORD_HASH` fingerprints source/business columns.
- `ETL_CONTROL` prevents reloading a successfully processed file version.
- Validated row count: **228,711**.

### Silver

Exactly eight business tables:

```text
SILVER_RECORD
SILVER_TIME
SILVER_POLICY
SILVER_CUSTOMER
SILVER_PRODUCT
SILVER_CHANNEL
SILVER_COVERAGE
SILVER_FINANCIAL
```

Technical staging: `DWH_SILVER.SILVER_STAGE`.

Silver uses Oracle MERGE/upsert at the frozen business grain; it is not SCD Type 2.

### Gold

Star schema:

```text
DIM_TIME
DIM_CUSTOMER
DIM_POLICY
DIM_PRODUCT
DIM_CHANNEL
FACT_POLICY
```

Validated row counts:

| Gold object | Rows |
|---|---:|
| FACT_POLICY | 228,711 |
| DIM_CUSTOMER | 100,453 |
| DIM_POLICY | 45,162 |
| DIM_PRODUCT | 5 |
| DIM_CHANNEL | 3 |
| DIM_TIME | 3 |

There is intentionally no `FACT_CLAIMS`: the source does not contain a claim-level business entity. `cost_claims_year` remains a policy-period measure in `FACT_POLICY`.

## Orchestration

The Python orchestration layer is in `src/orchestration/pipeline.py`; the Airflow DAG is `dags/insurance_risk_intelligence_pipeline.py`.

Execution dependency:

```text
BRONZE -> SILVER -> GOLD
```

The DAG uses `bronze >> silver >> gold`, `catchup=False`, `max_active_runs=1`, and `schedule=None`. It has been manually triggered successfully and remains unscheduled by design.

## FastAPI

The API is read-only and queries the Gold layer using the dedicated `DWH_API` database account.

| Method and route | Purpose |
|---|---|
| `GET /health` | Public API liveness |
| `GET /health/db` | Protected Oracle connectivity check |
| `GET /dashboard/summary` | Portfolio-level KPIs |
| `GET /dashboard/yearly` | Annual portfolio metrics |
| `GET /dashboard/products` | Product and reimbursement analysis |
| `GET /dashboard/channels` | Distribution-channel analysis |
| `GET /dashboard/policies` | Policy-type analysis |
| `GET /dashboard/customers` | Insured gender analysis |
| `GET /dashboard/customer-cohorts` | Insured effective-year cohorts |

Analytics routes and `/health/db` require the `X-API-Key` header. The server-side `API_ACCESS_KEY` must be configured; the API fails closed when it is missing. Optional CORS uses an exact allowlist in `API_CORS_ORIGINS` and defaults to no allowed origins.

## Streamlit dashboard

The dashboard is in `src/dashboard/` and consumes the existing API only. It does not connect directly to Oracle.

Six pages are available:

1. **Portfolio overview** — summary KPIs and annual premium, claims-cost, and exposure charts.
2. **Product analysis** — product type and reimbursement breakdowns.
3. **Channel analysis** — distribution-channel performance.
4. **Policy analysis** — policy type and policy DG breakdowns.
5. **Customer analysis** — customer dimension breakdown by gender.
6. **Customer cohort analysis** — cohorts by `YEAR_EFFECT_INSURED`, with interactive year-range filtering and trend charts.

The dashboard includes metric-definition tooltips, category comparison controls, chart value labels/tooltips, and detailed breakdown tables. See [docs/DASHBOARD.md](docs/DASHBOARD.md) for setup and page details.

### Run locally (Windows PowerShell)

From the repository root, activate your virtual environment and install dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the API in one terminal:

```powershell
$env:PYTHONPATH="$PWD\src"
$env:API_ACCESS_KEY="replace-with-a-long-random-secret"
uvicorn api.main:app --reload
```

Start the dashboard in a second terminal:

```powershell
$env:PYTHONPATH="$PWD\src"
$env:API_ACCESS_KEY="replace-with-the-same-secret"
# Optional when the API is not running at the default URL:
$env:API_BASE_URL="http://127.0.0.1:8000"
streamlit run src/dashboard/app.py
```

The API and dashboard must use the same API key. A project-root `.env` file can also provide local settings; do not commit secrets. The dashboard defaults to `http://127.0.0.1:8000`.

### Tests

Run the automated test suite from the repository root:

```powershell
$env:PYTHONPATH="$PWD\src"
pytest -q tests
```

API tests mock Oracle connections; they do not replace live Oracle or Gold reconciliation. Dashboard API-client tests mock HTTP responses.

## Security and configuration

- Do not commit database credentials, API keys, wallet files, or local driver files.
- The dashboard sends the API key from its server-side process; it is not embedded in browser-side chart code.
- Keep `API_CORS_ORIGINS` restricted to the exact origins that need access.
- Use a strong, unique API key outside local development.

## Validation record

The warehouse validation evidence is documented in [docs/VALIDATION.md](docs/VALIDATION.md). The Gold fact has 228,711 rows at the declared grain; dimension key uniqueness, fact foreign keys, fact key nulls, and Silver-to-Gold grain reconciliation were validated. Premium and Exposure reconciliation showed only small numeric precision differences.

The API was live-tested across its analytics routes, and the Streamlit dashboard was launched and visually tested locally. Airflow's DAG was manually executed successfully; no production schedule is claimed.

## Next phase

The next planned capability is an insurance intelligence assistant using an open-source LLM and retrieval-augmented generation (RAG), built on top of the existing Gold/API foundation. Frozen warehouse decisions remain unchanged.
