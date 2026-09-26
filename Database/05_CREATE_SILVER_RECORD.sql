/*
===============================================================================
File Name  : 05_CREATE_SILVER_RECORD.sql
Schema     : DWH_SILVER
Purpose    : Create Silver Record table
===============================================================================
*/

CREATE TABLE SILVER_RECORD
(
    ID                  VARCHAR2(100) NOT NULL,
    ID_POLICY           VARCHAR2(100) NOT NULL,
    ID_INSURED          VARCHAR2(100) NOT NULL,
    PERIOD              NUMBER       NOT NULL,
    RECORD_HASH         VARCHAR2(64)  NOT NULL,
    LOAD_ID             NUMBER       NOT NULL,
    LOAD_TIMESTAMP      TIMESTAMP    NOT NULL,
    SOURCE_FILE         VARCHAR2(500) NOT NULL,
    ETL_CREATED_BY      VARCHAR2(100) NOT NULL,

    CONSTRAINT PK_SILVER_RECORD
        PRIMARY KEY (ID_POLICY, ID_INSURED, PERIOD)
);

COMMENT ON TABLE SILVER_RECORD IS
'Silver record identity and technical lineage at the source business observation grain.';

COMMENT ON COLUMN SILVER_RECORD.ID IS
'Source record identifier.';

COMMENT ON COLUMN SILVER_RECORD.RECORD_HASH IS
'SHA-256 hash generated from the complete source record.';

COMMENT ON COLUMN SILVER_RECORD.LOAD_ID IS
'Bronze ETL execution identifier from which the record originated.';

COMMENT ON COLUMN SILVER_RECORD.SOURCE_FILE IS
'Source CSV filename.';

COMMIT;
