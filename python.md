Core Libraries
Pandas → Data manipulation, cleaning, transformation.

PySpark → Distributed big data processing.

SQLAlchemy → Database connections and ORM.

Airflow → Workflow orchestration.

Requests → API calls and data ingestion.

Boto3 → AWS integration (S3, Athena, Redshift).

## Data Ingestion
```python
# Read CSV
import pandas as pd
df = pd.read_csv("data.csv")

# Read JSON from API
import requests
response = requests.get("https://api.example.com/data")
data = response.json()

# Read from SQL
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@host/db")
df = pd.read_sql("SELECT * FROM table", engine)
```
## Data Transformation
```python
# Pandas transformations
df['amount'] = df['amount'].astype(float)
df['date'] = pd.to_datetime(df['date'])
df = df.dropna()

# PySpark transformations
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df_spark = spark.read.csv("data.csv", header=True, inferSchema=True)
df_spark = df_spark.filter(df_spark.amount > 100)
```
Data Loading
```python
# Write to CSV
df.to_csv("clean_data.csv", index=False)

# Write to SQL
df.to_sql("clean_table", engine, if_exists="replace", index=False)

# Write to S3
import boto3
s3 = boto3.client("s3")
s3.upload_file("clean_data.csv", "my-bucket", "clean_data.csv")
```
Workflow Orchestration (Airflow)
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    print("Extracting data...")

with DAG("etl_pipeline", start_date=datetime(2025,1,1), schedule_interval="@daily") as dag:
    task_extract = PythonOperator(task_id="extract", python_callable=extract)
```
## Useful Snippets
Environment variables:

```python
import os
db_user = os.getenv("DB_USER")
```
Logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
logging.info("Pipeline started")
```
Parallel processing:

```python
from multiprocessing import Pool
with Pool(4) as p:
    p.map(process_function, data_list)
```
## Quick Reference Table
|Task |	Library/Tool |Example |
|-- |-- |-- |
|Ingest CSV	|Pandas	|pd.read_csv() |
|Ingest API	|Requests	|requests.get()
|Ingest SQL	|SQLAlchemy	|pd.read_sql()
|Transform Data	|Pandas/PySpark	|df.dropna() / df_spark.filter()
|Load to DB	|SQLAlchemy	|df.to_sql()
|Load to S3	|Boto3	|s3.upload_file()
|Orchestrate	|Airflow	|PythonOperator


## pysparc
```python
from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("PySpark SQL Example") \
    .getOrCreate()
```
## Creating DataFrames
```python
# From Python list
data = [("Alice", 34), ("Bob", 45)]
df = spark.createDataFrame(data, ["name", "age"])

# From CSV
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# From JSON
df = spark.read.json("data.json")

# From Parquet
df = spark.read.parquet("data.parquet")
```
## Basic Operations
```python
# Show data
df.show()

# Select columns
df.select("name", "age").show()

# Filter rows
df.filter(df.age > 40).show()

# Group and aggregate
df.groupBy("age").count().show()

# Order by
df.orderBy(df.age.desc()).show()
```
## SQL Integration
``` python
# Register DataFrame as SQL table
df.createOrReplaceTempView("people")

# Run SQL query
result = spark.sql("SELECT name, age FROM people WHERE age > 40")
result.show()
```
## Common SQL Functions
```sql
-- Aggregations
SELECT COUNT(*), AVG(age), MAX(age), MIN(age) FROM people;

-- String functions
SELECT UPPER(name), LENGTH(name) FROM people;

-- Date functions
SELECT CURRENT_DATE, YEAR(order_date), MONTH(order_date) FROM orders;

-- Joins
SELECT o.id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id;
```
## Advanced Features
```python
# Adding new column
df = df.withColumn("age_plus_ten", df.age + 10)

# Casting
df = df.withColumn("age_str", df.age.cast("string"))

# Handling nulls
df.na.fill({"age": 0}).show()

# User Defined Function (UDF)
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

def add_one(x): return x + 1
    add_one_udf = udf(add_one, IntegerType())
    df = df.withColumn("age_plus_one", add_one_udf(df.age))
```
## Quick Reference Table
|Task	|PySpark Code	|SQL Equivalent
|-- |-- |
|Select columns	|df.select("col")	|SELECT col FROM table
|Filter rows	|df.filter(df.col > 10)	|WHERE col > 10
|Group & aggregate	|df.groupBy("col").count()	|GROUP BY col
|Order by	|df.orderBy(df.col.desc())	|ORDER BY col DESC
|Join tables	|df1.join(df2, "id")	|JOIN df2 ON df1.id = df2.id