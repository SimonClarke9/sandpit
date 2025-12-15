from pyspark.sql import SparkSession
import os


def main():    # Create a simple DataFrame
    print("CWD:", os.getcwd())

    spark = SparkSession.builder.appName("BasicCSVLoaderexample").getOrCreate()  

if __name__ == "__main__":
    main()
