# Validation

This document records the validated Bronze -> Silver -> Gold state as executed against the local Oracle environment.

## Bronze

Final validated Bronze count: **228,711**.

The final source is `BASE_DATA.csv`. The temporary `policy_test.csv` was removed because it introduced duplicate business-grain observations.

## Silver

Validated:

```text
Bronze rows                  228,711
Silver observation rows      228,711
Distinct periods                   3
Bronze -> Silver missing           0
Silver -> Bronze missing           0
Invalid observation keys            0
```

All eight Silver DQ checks passed, all eight MERGEs completed, and a rerun was validated without increasing Silver row counts.

## Gold execution

The complete pipeline executed successfully:

```text
python -m src.main

Gold ETL pipeline completed successfully. Fact rows: 228711
```

A Spark shutdown-hook temporary-directory cleanup error appeared after successful pipeline completion during process cleanup. It did not indicate a Gold data-load failure.

## Gold acceptance

### Row counts

```text
DIM_TIME             3
DIM_CUSTOMER   100,453
DIM_POLICY      45,162
DIM_PRODUCT          5
DIM_CHANNEL          3
FACT_POLICY     228,711
```

### Fact grain

```text
TOTAL_FACT_ROWS          228,711
DISTINCT_BUSINESS_KEYS   228,711
DUPLICATE_KEYS                 0
```

### Dimension business keys

All five Gold dimensions validated with zero duplicate business keys.

### Foreign-key integrity

```text
POLICY_KEY    0 invalid
CUSTOMER_KEY  0 invalid
PRODUCT_KEY   0 invalid
CHANNEL_KEY   0 invalid
TIME_KEY      0 invalid
```

### Silver -> Gold grain reconciliation

```text
SILVER_NOT_IN_GOLD = 0
GOLD_NOT_IN_SILVER = 0
```

### Fact null checks

All dimension keys and `ID_POLICY`, `ID_INSURED`, `PERIOD` validated with zero nulls.

### Period distribution

```text
2017 = 78,459
2018 = 73,970
2019 = 76,282
```

### Measure reconciliation

| Measure | Silver | Gold | Difference |
|---|---:|---:|---:|
| PREMIUM | 194864832.58909062 | 194864832.6043 | 0.01520938 |
| COST_CLAIMS_YEAR | 134405079.5435 | 134405079.5435 | 0 |
| EXPOSURE_TIME | 213938.168835801 | 213938.16884281 | 0.000007009 |
| N_MEDICAL_SERVICES | 3845156 | 3845156 | 0 |

The Premium and Exposure differences are very small numeric precision/scale effects from Gold Oracle numeric definitions. Grain, row counts, keys, and the remaining measures reconcile exactly.

## Gold acceptance decision

```text
IMPLEMENTED
EXECUTED
DQ VALIDATED
GRAIN RECONCILED
FK VALIDATED
MEASURE RECONCILED WITH NUMERIC PRECISION TOLERANCE
FROZEN
```

No additional profiling is required unless a future concrete defect is discovered.
