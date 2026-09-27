/*
===============================================================================
File Name  : 20_CREATE_GOLD_INDEXES.sql
Purpose    : Gold Star Schema supporting indexes
===============================================================================
*/

CREATE INDEX IDX_FACT_POLICY_POLICY
    ON FACT_POLICY (POLICY_KEY);

CREATE INDEX IDX_FACT_POLICY_CUSTOMER
    ON FACT_POLICY (CUSTOMER_KEY);

CREATE INDEX IDX_FACT_POLICY_PRODUCT
    ON FACT_POLICY (PRODUCT_KEY);

CREATE INDEX IDX_FACT_POLICY_CHANNEL
    ON FACT_POLICY (CHANNEL_KEY);

CREATE INDEX IDX_FACT_POLICY_TIME
    ON FACT_POLICY (TIME_KEY);

CREATE INDEX IDX_GOLD_STAGE_PERIOD
    ON GOLD_STAGE (PERIOD);

COMMIT;
