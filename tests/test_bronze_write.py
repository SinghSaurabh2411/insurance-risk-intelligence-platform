"""
===============================================================================
Project : Insurance Risk Intelligence Platform
File    : test_bronze_write.py
Purpose : Test Spark -> Oracle Bronze table write
===============================================================================
"""

from pyspark.sql import SparkSession

from utils.spark_session import create_spark_session

from config.oracle_config import (
    JDBC_URL,
    BRONZE_JDBC_PROPERTIES,
)

from config.config import (
    BRONZE_POLICY_TABLE_FQN,
)


def main():

    print("=" * 70)
    print("Spark -> Oracle Bronze Write Test")
    print("=" * 70)

    spark = None

    try:

        # =====================================================================
        # CREATE SPARK SESSION
        # =====================================================================

        spark = create_spark_session()

        print()
        print("Spark Session created successfully.")
        print("Spark version :", spark.version)

        # =====================================================================
        # CREATE TEST DATAFRAME
        # =====================================================================

        load_id = 999999
        test_data = [
            (
                "TEST_001",
                "TEST_POLICY_001",
                "TEST_INSURED_001",
                2026,
                load_id,
                "test_bronze_write.csv",
                "TEST_HASH_001",
            )
        ]

        test_columns = [
            "ID",
            "ID_POLICY",
            "ID_INSURED",
            "PERIOD",
            "LOAD_ID",
            "SOURCE_FILE",
            "RECORD_HASH",
        ]

        dataframe = spark.createDataFrame(
            test_data,
            test_columns,
        )

        print()
        print("Test DataFrame:")

        dataframe.show(
            truncate=False
        )

        # =====================================================================
        # WRITE TO ORACLE
        # =====================================================================

        print()
        print(
            "Writing test record to:",
            BRONZE_POLICY_TABLE_FQN,
        )

        (
            dataframe.write
            .format("jdbc")
            .option(
                "url",
                JDBC_URL,
            )
            .option(
                "dbtable",
                BRONZE_POLICY_TABLE_FQN,
            )
            .option(
                "user",
                BRONZE_JDBC_PROPERTIES["user"],
            )
            .option(
                "password",
                BRONZE_JDBC_PROPERTIES["password"],
            )
            .option(
                "driver",
                BRONZE_JDBC_PROPERTIES["driver"],
            )
            .mode("append")
            .save()
        )

        print()
        print("Bronze write successful.")

        # =====================================================================
        # READ BACK THE RECORD
        # =====================================================================

        print()
        print("Reading test record back from Oracle...")

        result = (
            spark.read
            .format("jdbc")
            .option(
                "url",
                JDBC_URL,
            )
            .option(
                "dbtable",
                BRONZE_POLICY_TABLE_FQN,
            )
            .option(
                "user",
                BRONZE_JDBC_PROPERTIES["user"],
            )
            .option(
                "password",
                BRONZE_JDBC_PROPERTIES["password"],
            )
            .option(
                "driver",
                BRONZE_JDBC_PROPERTIES["driver"],
            )
            .load()
            .filter(
                "ID = 'TEST_001'"
            )
        )

        result.show(
            truncate=False
        )

        print("=" * 70)
        print("BRONZE WRITE TEST PASSED")
        print("=" * 70)

    except Exception as exception:

        print("=" * 70)
        print("BRONZE WRITE TEST FAILED")
        print("=" * 70)

        print()
        print("Error:")
        print(exception)

        raise

    finally:

        if spark is not None:

            print()
            print("Stopping Spark Session...")

            spark.stop()

            print("Spark Session stopped.")


if __name__ == "__main__":

    main()