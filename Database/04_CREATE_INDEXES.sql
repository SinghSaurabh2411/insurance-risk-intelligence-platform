/*
===============================================================================
File Name  : 04_create_indexes.sql

Schema     : DWH_BRONZE

Purpose    : Create indexes for Bronze Layer

Description
-----------
Indexes required for:

• Incremental ETL
• MERGE Processing
• Record Change Detection
• Time-based filtering

===============================================================================
*/

-------------------------------------------------------------------------------
-- LOAD_ID
-------------------------------------------------------------------------------

CREATE INDEX IDX_BRONZE_LOAD_ID
ON BRONZE_POLICY_DATA (LOAD_ID);

-------------------------------------------------------------------------------
-- Business Grain
-------------------------------------------------------------------------------

CREATE INDEX IDX_BRONZE_GRAIN
ON BRONZE_POLICY_DATA
(
    ID_POLICY,
    ID_INSURED,
    PERIOD
);

-------------------------------------------------------------------------------
-- Record Hash
-------------------------------------------------------------------------------

CREATE INDEX IDX_BRONZE_RECORD_HASH
ON BRONZE_POLICY_DATA (RECORD_HASH);

-------------------------------------------------------------------------------
-- Period
-------------------------------------------------------------------------------

CREATE INDEX IDX_BRONZE_PERIOD
ON BRONZE_POLICY_DATA (PERIOD);

COMMIT;