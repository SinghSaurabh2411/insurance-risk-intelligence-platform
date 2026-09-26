/*
===============================================================================
File Name  : 06_CREATE_SILVER_TIME.sql
Schema     : DWH_SILVER
Purpose    : Create Silver Time table
===============================================================================
*/

CREATE TABLE SILVER_TIME
(
    PERIOD                  NUMBER NOT NULL,
    YEAR_EFFECT_INSURED     NUMBER,
    YEAR_LAPSE_INSURED      NUMBER,
    YEAR_EFFECT_POLICY      NUMBER,
    YEAR_LAPSE_POLICY       NUMBER,

    CONSTRAINT PK_SILVER_TIME
        PRIMARY KEY (PERIOD)
);

COMMENT ON TABLE SILVER_TIME IS
'Silver time subject containing calendar attributes associated with each observation period.';

COMMIT;
