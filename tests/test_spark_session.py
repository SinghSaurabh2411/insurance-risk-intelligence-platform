from src.utils.spark_session import create_spark_session


def main():

    print("=" * 70)
    print("Testing Spark Session")
    print("=" * 70)

    spark = None

    try:

        spark = create_spark_session()

        print()
        print("Spark Session created successfully.")
        print("Spark version :", spark.version)
        print("Spark master  :", spark.sparkContext.master)

        print()
        print("Spark Session test PASSED.")

    except Exception as exception:

        print()
        print("Spark Session test FAILED.")
        print(exception)

        raise

    finally:

        if spark is not None:

            spark.stop()

            print()
            print("Spark Session stopped.")


if __name__ == "__main__":
    main()