/*****************************************************************************************
 Project        : Insurance Risk Intelligence Platform
 File           : 01_create_users.sql
 Layer          : Oracle Database
 Purpose        : Create schemas for Medallion Architecture

 Author         : Saurabh Singh
 Created On     : 2026-06-28

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
IDENTIFIED BY bronze123
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
IDENTIFIED BY silver123
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
IDENTIFIED BY gold123
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



/*****************************************************************************************
END OF SCRIPT
*****************************************************************************************/