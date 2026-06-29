/*
===============================================================================
File Name  : 03_CREATE_BRONZE_POLICY_DATA.sql

Schema     : BRONZE_DWH

Purpose    : Create Bronze Policy Data Table

Description
-----------
Raw landing table for Healthcare Insurance dataset.

• Stores source data exactly as received.
• No transformations.
• No deduplication.
• No business validations.
• Includes ETL audit columns.

Grain
-----
(ID_POLICY, ID_INSURED, PERIOD)

===============================================================================
*/

-- CONNECT BRONZE_DWH/<password>;

CREATE TABLE BRONZE_POLICY_DATA
(

    ----------------------------------------------------------------------------
    -- Source Columns
    ----------------------------------------------------------------------------

    ID                      VARCHAR2(100),

    ID_POLICY               VARCHAR2(100),

    ID_INSURED              VARCHAR2(100),

    PERIOD                  NUMBER,

    DATE_EFFECT_INSURED     DATE,

    DATE_LAPSE_INSURED      DATE,

    DATE_EFFECT_POLICY      DATE,

    DATE_LAPSE_POLICY       DATE,

    YEAR_EFFECT_INSURED     NUMBER,

    YEAR_LAPSE_INSURED      NUMBER,

    YEAR_EFFECT_POLICY      NUMBER,

    YEAR_LAPSE_POLICY       NUMBER,

    EXPOSURE_TIME           NUMBER,

    LAPSE                   NUMBER,

    SENIORITY_INSURED       NUMBER,

    SENIORITY_POLICY        NUMBER,

    TYPE_POLICY             VARCHAR2(20),

    TYPE_POLICY_DG          VARCHAR2(20),

    TYPE_PRODUCT            VARCHAR2(20),

    REIMBURSEMENT           VARCHAR2(10),

    NEW_BUSINESS            NUMBER,

    DISTRIBUTION_CHANNEL    VARCHAR2(20),

    GENDER                  VARCHAR2(5),

    AGE                     NUMBER,

    PREMIUM                 NUMBER,

    COST_CLAIMS_YEAR        NUMBER,

    N_MEDICAL_SERVICES      NUMBER,

    N_INSURED_PC            NUMBER,

    N_INSURED_MUN           NUMBER,

    N_INSURED_PROV          NUMBER,

    IICIMUN                 NUMBER,

    IICIPROV                NUMBER,

    C_H                     VARCHAR2(10),

    C_GI                    NUMBER,

    C_II                    NUMBER,

    C_IE_P                  NUMBER,

    C_IE_S                  NUMBER,

    C_IE_T                  NUMBER,

    C_GE_P                  NUMBER,

    C_GE_S                  NUMBER,

    C_GE_T                  NUMBER,

    C_C                     VARCHAR2(10),

    ----------------------------------------------------------------------------
    -- Audit Columns
    ----------------------------------------------------------------------------

    LOAD_ID                 NUMBER           NOT NULL,

    LOAD_TIMESTAMP          TIMESTAMP        DEFAULT SYSTIMESTAMP NOT NULL,

    SOURCE_FILE            VARCHAR2(500)    NOT NULL,

    RECORD_HASH            VARCHAR2(64)     NOT NULL,

    ETL_CREATED_BY         VARCHAR2(100)
                           DEFAULT 'PYSPARK_ETL'
                           NOT NULL

);

-------------------------------------------------------------------------------
-- Table Comment
-------------------------------------------------------------------------------

COMMENT ON TABLE BRONZE_POLICY_DATA IS
'Raw Bronze layer storing source insurance dataset without transformations.';

-------------------------------------------------------------------------------
-- Audit Column Comments
-------------------------------------------------------------------------------

COMMENT ON COLUMN BRONZE_POLICY_DATA.LOAD_ID IS
'Unique ETL execution identifier.';

COMMENT ON COLUMN BRONZE_POLICY_DATA.LOAD_TIMESTAMP IS
'Timestamp when record was loaded into Bronze.';

COMMENT ON COLUMN BRONZE_POLICY_DATA.SOURCE_FILE IS
'Source CSV filename.';

COMMENT ON COLUMN BRONZE_POLICY_DATA.RECORD_HASH IS
'SHA-256 hash generated from the complete source record.';

COMMENT ON COLUMN BRONZE_POLICY_DATA.ETL_CREATED_BY IS
'ETL framework responsible for loading the record.';

COMMIT;