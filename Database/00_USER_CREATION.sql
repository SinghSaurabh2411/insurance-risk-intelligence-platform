/*****************************************************************************************
 Project        : Healthcare Insurance Data Warehouse
 File           : 01_create_users.sql
 Layer          : Oracle Database
 Purpose        : Create schemas for Medallion Architecture

 Author         : Saurabh Singh
 Created On     : YYYY-MM-DD

 Schemas
 --------
 DWH_BRONZE
 DWH_SILVER
 DWH_GOLD

*****************************************************************************************/


/*****************************************************************************************
DROP USERS (Execute only if recreating the environment)
*****************************************************************************************/

-- DROP USER DWH_GOLD CASCADE;
-- DROP USER DWH_SILVER CASCADE;
-- DROP USER DWH_BRONZE CASCADE;



/*****************************************************************************************
CREATE BRONZE USER
*****************************************************************************************/

CREATE USER DWH_BRONZE
IDENTIFIED BY saurabh
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA UNLIMITED ON USERS;

GRANT
    CREATE SESSION,
    CREATE TABLE,
    CREATE VIEW,
    CREATE SEQUENCE,
    CREATE PROCEDURE,
    CREATE TRIGGER,
    CREATE SYNONYM
TO DWH_BRONZE;



/*****************************************************************************************
CREATE SILVER USER
*****************************************************************************************/

CREATE USER DWH_SILVER
IDENTIFIED BY saurabh
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA UNLIMITED ON USERS;

GRANT
    CREATE SESSION,
    CREATE TABLE,
    CREATE VIEW,
    CREATE SEQUENCE,
    CREATE PROCEDURE,
    CREATE TRIGGER,
    CREATE SYNONYM
TO DWH_SILVER;



/*****************************************************************************************
CREATE GOLD USER
*****************************************************************************************/

CREATE USER DWH_GOLD
IDENTIFIED BY saurabh
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA UNLIMITED ON USERS;

GRANT
    CREATE SESSION,
    CREATE TABLE,
    CREATE VIEW,
    CREATE SEQUENCE,
    CREATE PROCEDURE,
    CREATE TRIGGER,
    CREATE SYNONYM
TO DWH_GOLD;

/*
===============================================================================
Create DWH Control Schema

Description
-----------
Creates the schema responsible for ETL metadata, audit,
control tables and sequences.

===============================================================================
*/


CREATE USER DWH_CONTROL
IDENTIFIED BY saurabh
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA UNLIMITED ON USERS;

------------------------------------------------------------
-- Required Privileges
------------------------------------------------------------

GRANT CREATE SESSION TO DWH_CONTROL;

GRANT CREATE TABLE TO DWH_CONTROL;

GRANT CREATE VIEW TO DWH_CONTROL;

GRANT CREATE SEQUENCE TO DWH_CONTROL;

GRANT CREATE PROCEDURE TO DWH_CONTROL;

GRANT CREATE TRIGGER TO DWH_CONTROL;

GRANT CREATE SYNONYM TO DWH_CONTROL;

GRANT UNLIMITED TABLESPACE TO DWH_CONTROL;

COMMIT;

/*****************************************************************************************
END OF SCRIPT
*****************************************************************************************/