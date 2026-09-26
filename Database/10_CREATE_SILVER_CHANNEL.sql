/*
===============================================================================
File Name  : 10_CREATE_SILVER_CHANNEL.sql
Schema     : DWH_SILVER
Purpose    : Create Silver Channel table
Grain      : (ID_POLICY, ID_INSURED, PERIOD)
===============================================================================
*/

CREATE TABLE SILVER_CHANNEL
(
    ID_POLICY               VARCHAR2(100) NOT NULL,
    ID_INSURED              VARCHAR2(100) NOT NULL,
    PERIOD                  NUMBER       NOT NULL,
    DISTRIBUTION_CHANNEL    VARCHAR2(20),

    CONSTRAINT PK_SILVER_CHANNEL
        PRIMARY KEY (ID_POLICY, ID_INSURED, PERIOD)
);

COMMENT ON TABLE SILVER_CHANNEL IS
'Silver distribution channel subject at the source business observation grain.';

COMMIT;
