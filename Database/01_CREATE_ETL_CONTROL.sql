/*
===============================================================================
File Name  : 01_create_etl_control.sql

Schema     : DWH_CONTROL

Purpose    : Stores metadata for every ETL execution

===============================================================================
*/

------------------------------------------------------------
-- Connect
------------------------------------------------------------
-- CONNECT DWH_CONTROL/<password>

CREATE TABLE ETL_CONTROL
(
    LOAD_ID                 NUMBER              NOT NULL,

    LAYER_NAME              VARCHAR2(20)        NOT NULL,

    PIPELINE_NAME           VARCHAR2(100)       NOT NULL,

    SOURCE_FILE             VARCHAR2(500)       NOT NULL,

    SOURCE_FILE_HASH        VARCHAR2(64)        NOT NULL,

    SOURCE_RECORD_COUNT     NUMBER,

    TARGET_RECORD_COUNT     NUMBER,

    LOAD_STATUS             VARCHAR2(20)        NOT NULL,

    START_TIME              TIMESTAMP           NOT NULL,

    END_TIME                TIMESTAMP,

    ERROR_MESSAGE           VARCHAR2(4000),

    CREATED_BY              VARCHAR2(100)
                                DEFAULT 'PYSPARK_ETL'
                                NOT NULL,

    CONSTRAINT PK_ETL_CONTROL
        PRIMARY KEY (LOAD_ID),

    CONSTRAINT CHK_LOAD_STATUS
        CHECK
        (
            LOAD_STATUS IN
            (
                'STARTED',
                'SUCCESS',
                'FAILED'
            )
        )
);

------------------------------------------------------------
-- Comments
------------------------------------------------------------

COMMENT ON TABLE ETL_CONTROL IS
'Stores ETL execution metadata for Bronze, Silver and Gold pipelines.';

COMMENT ON COLUMN ETL_CONTROL.LOAD_ID IS
'Unique ETL execution identifier';

COMMENT ON COLUMN ETL_CONTROL.LAYER_NAME IS
'Pipeline Layer';

COMMENT ON COLUMN ETL_CONTROL.PIPELINE_NAME IS
'Pipeline Name';

COMMENT ON COLUMN ETL_CONTROL.SOURCE_FILE IS
'Source CSV File';

COMMENT ON COLUMN ETL_CONTROL.SOURCE_FILE_HASH IS
'SHA-256 checksum of source file';

COMMENT ON COLUMN ETL_CONTROL.SOURCE_RECORD_COUNT IS
'Records read from source';

COMMENT ON COLUMN ETL_CONTROL.TARGET_RECORD_COUNT IS
'Records successfully loaded';

COMMENT ON COLUMN ETL_CONTROL.LOAD_STATUS IS
'Execution Status';

COMMENT ON COLUMN ETL_CONTROL.START_TIME IS
'Execution Start Timestamp';

COMMENT ON COLUMN ETL_CONTROL.END_TIME IS
'Execution End Timestamp';

COMMENT ON COLUMN ETL_CONTROL.ERROR_MESSAGE IS
'Failure Message';

COMMENT ON COLUMN ETL_CONTROL.CREATED_BY IS
'ETL Framework';

COMMIT;