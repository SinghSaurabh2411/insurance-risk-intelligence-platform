/*
===============================================================================
File Name  : 19_CREATE_GOLD_STAGE.sql
Schema     : DWH_GOLD
Purpose    : Technical staging table for Gold dimensionalization
Note       : This is not a business Gold table.
===============================================================================
*/

CREATE TABLE GOLD_STAGE
(
    ID_POLICY               VARCHAR2(100) NOT NULL,
    ID_INSURED              VARCHAR2(100) NOT NULL,
    PERIOD                  NUMBER NOT NULL,

    DATE_EFFECT_INSURED     DATE,
    DATE_LAPSE_INSURED      DATE,
    YEAR_EFFECT_INSURED     NUMBER,
    YEAR_LAPSE_INSURED      NUMBER,
    GENDER                  VARCHAR2(5),
    AGE                     NUMBER,

    DATE_EFFECT_POLICY      DATE,
    DATE_LAPSE_POLICY       DATE,
    YEAR_EFFECT_POLICY      NUMBER,
    YEAR_LAPSE_POLICY       NUMBER,
    SENIORITY_POLICY        NUMBER,
    TYPE_POLICY             VARCHAR2(20),
    TYPE_POLICY_DG          VARCHAR2(20),
    NEW_BUSINESS            NUMBER,
    LAPSE                   NUMBER,

    TYPE_PRODUCT            VARCHAR2(20) NOT NULL,
    REIMBURSEMENT           VARCHAR2(10) NOT NULL,
    DISTRIBUTION_CHANNEL    VARCHAR2(20) NOT NULL,

    EXPOSURE_TIME           NUMBER,
    N_MEDICAL_SERVICES      NUMBER,
    PREMIUM                 NUMBER,
    COST_CLAIMS_YEAR        NUMBER,

    LOAD_ID                 NUMBER NOT NULL,
    LOAD_TIMESTAMP          TIMESTAMP NOT NULL,
    SOURCE_FILE             VARCHAR2(500) NOT NULL,
    RECORD_HASH             VARCHAR2(64) NOT NULL,
    ETL_CREATED_BY          VARCHAR2(100) NOT NULL,

    CONSTRAINT PK_GOLD_STAGE PRIMARY KEY (ID_POLICY, ID_INSURED, PERIOD)
);

COMMENT ON TABLE GOLD_STAGE IS
'Technical Gold staging table; not part of the business Star Schema.';

COMMIT;
