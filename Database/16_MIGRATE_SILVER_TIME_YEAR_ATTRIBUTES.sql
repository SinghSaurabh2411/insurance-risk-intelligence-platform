/*
===============================================================================
File Name  : 16_MIGRATE_SILVER_TIME_YEAR_ATTRIBUTES.sql
Purpose    : Move observation-level year attributes from SILVER_TIME into
             SILVER_POLICY and SILVER_CUSTOMER.
Reason     : YEAR_* attributes vary within PERIOD and therefore are not
             period-level attributes.
===============================================================================
*/

ALTER TABLE SILVER_POLICY
    ADD (
        YEAR_EFFECT_POLICY NUMBER,
        YEAR_LAPSE_POLICY  NUMBER
    );

ALTER TABLE SILVER_CUSTOMER
    ADD (
        YEAR_EFFECT_INSURED NUMBER,
        YEAR_LAPSE_INSURED  NUMBER
    );

ALTER TABLE SILVER_TIME
    DROP COLUMN YEAR_EFFECT_INSURED;

ALTER TABLE SILVER_TIME
    DROP COLUMN YEAR_LAPSE_INSURED;

ALTER TABLE SILVER_TIME
    DROP COLUMN YEAR_EFFECT_POLICY;

ALTER TABLE SILVER_TIME
    DROP COLUMN YEAR_LAPSE_POLICY;

COMMIT;
