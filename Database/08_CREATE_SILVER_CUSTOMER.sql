/*
===============================================================================
File Name  : 08_CREATE_SILVER_CUSTOMER.sql
Schema     : DWH_SILVER
Purpose    : Create Silver Customer table
Grain      : (ID_POLICY, ID_INSURED, PERIOD)
===============================================================================
*/

CREATE TABLE SILVER_CUSTOMER
(
    ID_INSURED              VARCHAR2(100) NOT NULL,
    ID_POLICY               VARCHAR2(100) NOT NULL,
    PERIOD                  NUMBER       NOT NULL,
    DATE_EFFECT_INSURED     DATE,
    DATE_LAPSE_INSURED      DATE,
    SENIORITY_INSURED       NUMBER,
    GENDER                  VARCHAR2(5),
    AGE                     NUMBER,

    CONSTRAINT PK_SILVER_CUSTOMER
        PRIMARY KEY (ID_POLICY, ID_INSURED, PERIOD)
);

COMMENT ON TABLE SILVER_CUSTOMER IS
'Silver customer subject at the source business observation grain.';

COMMIT;
