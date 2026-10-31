-- =============================================================================
-- Project : Insurance Risk Intelligence Platform
-- File    : 22_CREATE_API_USER.sql
-- Purpose : Create a dedicated read-only Oracle account for the API.
-- =============================================================================
--
-- IMPORTANT:
-- 1. Execute this script using an Oracle account with CREATE USER and GRANT
--    privileges.
-- 2. Replace the password placeholder with a strong, unique password before
--    execution. Do not commit the real password to source control.
-- 3. The API account receives access only to the six approved Gold tables.
--
-- =============================================================================

CREATE USER DWH_API
IDENTIFIED BY "REPLACE_WITH_A_STRONG_UNIQUE_PASSWORD";

GRANT CREATE SESSION TO DWH_API;

GRANT SELECT ON DWH_GOLD.DIM_TIME TO DWH_API;
GRANT SELECT ON DWH_GOLD.DIM_CUSTOMER TO DWH_API;
GRANT SELECT ON DWH_GOLD.DIM_POLICY TO DWH_API;
GRANT SELECT ON DWH_GOLD.DIM_PRODUCT TO DWH_API;
GRANT SELECT ON DWH_GOLD.DIM_CHANNEL TO DWH_API;
GRANT SELECT ON DWH_GOLD.FACT_POLICY TO DWH_API;

-- No INSERT, UPDATE, DELETE, or schema ownership privileges are granted.
