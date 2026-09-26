/*
===============================================================================
File Name  : 06_CREATE_SILVER_TIME.sql
Schema     : DWH_SILVER
Purpose    : Create Silver Time table
Grain      : PERIOD
===============================================================================
*/

CREATE TABLE SILVER_TIME
(
    PERIOD NUMBER NOT NULL,

    CONSTRAINT PK_SILVER_TIME
        PRIMARY KEY (PERIOD)
);

COMMENT ON TABLE SILVER_TIME IS
'Silver time subject containing one row per observation period.';

COMMIT;
