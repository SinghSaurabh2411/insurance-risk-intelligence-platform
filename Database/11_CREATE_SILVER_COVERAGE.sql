/*
===============================================================================
File Name  : 11_CREATE_SILVER_COVERAGE.sql
Schema     : DWH_SILVER
Purpose    : Create Silver Coverage table
Grain      : (ID_POLICY, ID_INSURED, PERIOD)
===============================================================================
*/

CREATE TABLE SILVER_COVERAGE
(
    ID_POLICY               VARCHAR2(100) NOT NULL,
    ID_INSURED              VARCHAR2(100) NOT NULL,
    PERIOD                  NUMBER       NOT NULL,
    EXPOSURE_TIME           NUMBER,
    N_MEDICAL_SERVICES      NUMBER,

    CONSTRAINT PK_SILVER_COVERAGE
        PRIMARY KEY (ID_POLICY, ID_INSURED, PERIOD)
);

COMMENT ON TABLE SILVER_COVERAGE IS
'Silver coverage subject containing exposure and annual service measures at the source business observation grain.';

COMMIT;
