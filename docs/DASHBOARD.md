# Streamlit Dashboard

## Purpose and data flow

The Streamlit application provides an interactive presentation layer for the existing Insurance Risk Intelligence API. It does not connect directly to Oracle and does not implement independent business calculations beyond presentation-level aggregation and formatting.

```text
Oracle Gold star schema
        |
        v
Authenticated FastAPI analytics endpoints
        |
        v
Streamlit dashboard (src/dashboard/)
```

The dashboard uses the seven analytics endpoints already exposed by FastAPI:

| API route | Dashboard use |
|---|---|
| `GET /dashboard/summary` | Portfolio KPI cards |
| `GET /dashboard/yearly` | Annual premium, claims cost, and exposure trends |
| `GET /dashboard/products` | Product type and reimbursement analysis |
| `GET /dashboard/channels` | Distribution-channel analysis |
| `GET /dashboard/policies` | Policy type and policy DG analysis |
| `GET /dashboard/customers` | Customer breakdown by gender |
| `GET /dashboard/customer-cohorts` | Insured effective-year cohort analysis |

## Pages

### Portfolio overview

Displays total policies, total observations, total premium, total claims cost, average premium, and total exposure. The reporting period is derived from the years returned by the yearly endpoint. Three annual charts show premium and claims cost in ₹ millions and exposure in its source measure.

### Product analysis

Groups the product endpoint by product type and reimbursement category. Users can select a measure for category comparison and inspect the detailed breakdown table.

### Channel analysis

Compares distribution channels using the same supported measures and detailed breakdown table.

### Policy analysis

Groups the policy endpoint by policy type and policy DG classification.

### Customer analysis

Presents customer dimension breakdowns by the gender attribute returned by the API, including customer records and premium charts.

### Customer cohort analysis

Groups records by `YEAR_EFFECT_INSURED`, the year insurance became effective for the insured. This cohort year is distinct from the annual reporting `PERIOD` in the overview. Interactive line charts avoid overcrowding across the full historical cohort range; the year-range slider filters the charts, while the detailed table retains all returned cohort records.

## Metric interpretation

Metric definitions are available through the dashboard's information tooltips. Important grain considerations:

- **Total policies:** distinct policy IDs in the relevant result. A policy can occur in more than one reporting period.
- **Total observations:** policy-insured-period records at the Gold fact grain `(ID_POLICY, ID_INSURED, PERIOD)`.
- **Average premium:** average premium per policy-insured-period observation, not per unique policy.
- **Customer records:** customer dimension records represented in the relevant endpoint result.
- **Total exposure:** sum of the source exposure-time measure; interpret its unit according to the source dataset.
- **Cohort year:** `YEAR_EFFECT_INSURED`, not the fact reporting period.

Category-level distinct policy counts can overlap across categories. They must not be summed to claim a distinct portfolio-wide policy count. The dashboard therefore presents additive observation and financial totals on category pages and retains category-level policy counts in the detail table.

## Configuration

The dashboard uses the server-side configuration in `src/dashboard/config.py`:

| Environment variable | Default / purpose |
|---|---|
| `API_BASE_URL` | Defaults to `http://127.0.0.1:8000` |
| `API_ACCESS_KEY` | Required; sent as `X-API-Key` from the dashboard server process |

The API key may be supplied through the process environment, a project-root `.env` file, or Streamlit secrets. Never commit credentials or expose the key in client-side code.

## Local startup (Windows PowerShell)

Run from the repository root with the project's virtual environment activated.

Terminal 1 — API:

```powershell
$env:PYTHONPATH="$PWD\src"
$env:API_ACCESS_KEY="replace-with-a-long-random-secret"
uvicorn api.main:app --reload
```

Terminal 2 — dashboard:

```powershell
$env:PYTHONPATH="$PWD\src"
$env:API_ACCESS_KEY="replace-with-the-same-secret"
# Set only if FastAPI is hosted at a non-default address:
$env:API_BASE_URL="http://127.0.0.1:8000"
streamlit run src/dashboard/app.py
```

The API and dashboard must use the same key. Keep the API process running while using the dashboard.

## Caching and refresh

API responses are cached by Streamlit for five minutes. The sidebar refresh action clears the endpoint cache and reruns the dashboard.

## Tests

Dashboard API-client tests are in `tests/test_dashboard_api_client.py`. Run the suite from the repository root:

```powershell
$env:PYTHONPATH="$PWD\src"
pytest -q tests
```

The client tests mock HTTP responses. They do not replace live API, Oracle, or Gold-layer validation.
