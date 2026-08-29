from src.utils.spark_session import create_spark_session

from config.oracle_config import (
    JDBC_URL,
    CONTROL_JDBC_PROPERTIES,
)


def main():

    print("=" * 70)
    print("Spark -> Oracle JDBC Connectivity Test")
    print("=" * 70)

    spark = None

    try:
        # CREATE SPARK SESSION
        spark = create_spark_session()
        print("\nSpark Session created successfully.")
        print("Spark version :", spark.version)

        # ORACLE QUERY
        query = """
        (
            SELECT
                USER AS CURRENT_USER,
                SYSDATE AS CURRENT_DATE
            FROM DUAL
        ) TEST_QUERY
        """

        print("\nConnecting to Oracle...")
        print("JDBC URL :", JDBC_URL)
        print("Oracle user :", CONTROL_JDBC_PROPERTIES["user"])

        # READ FROM ORACLE
        dataframe = (
            spark.read
            .format("jdbc")
            .option("url", JDBC_URL)
            .option("dbtable", query)
            .option("user", CONTROL_JDBC_PROPERTIES["user"])
            .option("password", CONTROL_JDBC_PROPERTIES["password"])
            .option("driver", CONTROL_JDBC_PROPERTIES["driver"])
            .load()
        )

        print("\nOracle JDBC connection successful.")
        dataframe.show(truncate=False)

        print("=" * 70)
        print("JDBC TEST PASSED")
        print("=" * 70)

    except Exception as exception:
        print("=" * 70)
        print("JDBC TEST FAILED")
        print("=" * 70)
        print("\nError:")
        print(exception)
        raise

    finally:
        if spark is not None:
            print("\nStopping Spark Session...")
            spark.stop()
            print("Spark Session stopped.")


if __name__ == "__main__":
    main()
