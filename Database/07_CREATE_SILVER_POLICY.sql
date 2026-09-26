/*
===============================================================================
File Name  : 07_CREATE_SILVER_POLICY.sql
Schema     : DWH_SILVER
Purpose    : Create Silver Policy table
Grain      : (ID_POLICY, ID_INSURED, PERIOD)
===============================================================================
*/

CREATE TABLE SILVER_POLICY
(
    ID_POLICY               VARCHAR2(100) NOT NULL,
    ID_INSURED              VARCHAR2(100) NOT NULL,
    PERIOD                  NUMBER       NOT NULL,
    DATE_EFFECT_POLICY      DATE,
    DATE_LAPSE_POLICY       DATE,
    SENIORITY_POLICY        NUMBER,
    TYPE_POLICY             VARCHAR2(20),
    TYPE_POLICY_DG          VARCHAR2(20),
    NEW_BUSINESS            NUMBER,
    LAPSE                   NUMBER,

    CONSTRAINT PK_SILVER_POLICY
        PRIMARY KEY (ID_POLICY, ID_INSURED, PERIOD)
);

COMMENT ON TABLE SILVER_POLICY IS
'Silver policy subject at the source business observation grain.';

COMMIT;
