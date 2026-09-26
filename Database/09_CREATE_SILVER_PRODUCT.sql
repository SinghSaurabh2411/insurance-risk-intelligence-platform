/*
===============================================================================
File Name  : 09_CREATE_SILVER_PRODUCT.sql
Schema     : DWH_SILVER
Purpose    : Create Silver Product table
Grain      : (ID_POLICY, ID_INSURED, PERIOD)
===============================================================================
*/

CREATE TABLE SILVER_PRODUCT
(
    ID_POLICY               VARCHAR2(100) NOT NULL,
    ID_INSURED              VARCHAR2(100) NOT NULL,
    PERIOD                  NUMBER       NOT NULL,
    TYPE_PRODUCT            VARCHAR2(20),
    REIMBURSEMENT            VARCHAR2(10),

    CONSTRAINT PK_SILVER_PRODUCT
        PRIMARY KEY (ID_POLICY, ID_INSURED, PERIOD)
);

COMMENT ON TABLE SILVER_PRODUCT IS
'Silver product subject at the source business observation grain.';

COMMIT;
