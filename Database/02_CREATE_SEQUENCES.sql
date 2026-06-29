/*
===============================================================================
File Name  : 02_create_sequences.sql

Schema     : DWH_CONTROL

Purpose    : Create Oracle Sequences

===============================================================================
*/

------------------------------------------------------------
-- Connect
------------------------------------------------------------
-- CONNECT DWH_CONTROL/<password>

CREATE SEQUENCE SEQ_LOAD_ID
START WITH 1
INCREMENT BY 1
MINVALUE 1
NOCACHE
NOCYCLE;

GRANT SELECT ON DWH_CONTROL.ETL_CONTROL TO DWH_BRONZE;
GRANT SELECT ON DWH_CONTROL.SEQ_LOAD_ID TO DWH_BRONZE;

COMMIT;