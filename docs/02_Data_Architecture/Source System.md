# Source System

## Purpose

This document records the source format and ingestion behavior evidenced by the committed repository code.

## Source file

The repository's current source dataset is:

```text
data/raw/BASE_DATA.csv
```

The Bronze loader reads CSV files from the configured Bronze source directory. It uses the configured header and delimiter settings, disables schema inference, and reads values before applying explicit Bronze transformations.

The current repository also contains sample data under `data/sample/`; that sample workbook is not the file read by the committed Bronze loader in the current source configuration.

## Source-to-Bronze target

The Bronze loader writes transformed source records to:

```text
DWH_BRONZE.BRONZE_POLICY_DATA
```

The Bronze DDL defines the target structure. The Python validation and transformation modules define the source schema expectations and transformation behavior. Do not use an older document's source-column count or attribute descriptions as implementation evidence without reconciling them to `src/bronze/bronze_validator.py` and `src/bronze/bronze_transform.py`.

## Ingestion and file-version control

The current loader:
1. Discovers unprocessed source files.
2. Calculates SHA-256 from the complete file bytes.
3. Reads the CSV.
4. Registers the load in `ETL_CONTROL`.
5. Validates and transforms the source data.
6. Writes the result to Bronze.
7. Marks the load `SUCCESS`, or `FAILED` when processing raises an exception.

The file handler/control-table implementation checks prior successful processing using source filename and source-file hash. The hash identifies file content, not individual rows.

`RECORD_HASH` is generated separately for a transformed source record. It must not be confused with `SOURCE_FILE_HASH`.

## Bronze write behavior

The Bronze write mode is configured in Python configuration and used by the JDBC writer. The current design is append-oriented. No Delta Lake table or Delta Lake MERGE implementation is present in the Bronze loader.

## Downstream mapping

The Bronze source is projected into the eight Silver tables defined by `SILVER_PROJECTIONS` in `src/silver/silver_transform.py`. The exact projected columns and their target grains are documented in `Data Model.md` and the Silver DDL files.

The implemented Silver business subjects are record, time, policy, customer, product, channel, coverage and financial. The current code does not define `SILVER_CLAIMS` or `SILVER_ENRICHMENT`.

Gold is built from those eight Silver tables by `src/gold/gold_transform.py` and `src/gold/gold_loader.py`. The implemented Gold objects are five dimensions and `FACT_POLICY`.

## Source semantics and limitations

This document does not infer the business meaning, units, null semantics, or statistical interpretation of individual source attributes. Use the source data dictionary and verify ambiguous definitions with the dataset documentation before encoding them as business rules or RAG facts.

No CDC feed, streaming source, or operational source-system connector is asserted by the current CSV ingestion code.
