/*
===============================================================================
File Name  : 12_CREATE_SILVER_FINANCIAL.sql
Schema     : DWH_SILVER
Purpose    : Create Silver Financial table
Grain      : (ID_POLICY, ID_INSURED, PERIOD)
===============================================================================
*/

CREATE TABLE SILVER_FINANCIAL
(
    ID_POLICY               VARCHAR2(100) NOT NULL,
    ID_INSURED              VARCHAR2(100) NOT NULL,
    PERIOD                  NUMBER       NOT NULL,
    PREMIUM                 NUMBER,
    COST_CLAIMS_YEAR        NUMBER,

    CONSTRAINT PK_SILVER_FINANCIAL
        PRIMARY KEY (ID_POLICY, ID_INSURED, PERIOD)
);

COMMENT ON TABLE SILVER_FINANCIAL IS
'Silver financial subject containing annual premium and healthcare claims cost at the source business observation grain.';

COMMIT;
