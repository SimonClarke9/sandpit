# Advantages of PySpack over Python
- scalability for handling large datasets
- high performance through parrallel processing
- fault tolerance
- Integration with other Apache tools


# Create a basic Spark session

import pyspark.sql from SparkSession

```python
import logging
import pyspark.sql imort SparkSession

# start logging:
logging.basicConfig( level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s" )
logger = logging.getLogger(__name__))


spark = SparkSession.builder.appName('MyAppName').getOrCreate()
# or

# local[*]  - use all cores in the local machine. 
# If you know the local machine as n cores then you cal adjust like this: 'local[16]'
spark = SparkSession.builder.appName('MyAppName').master('local[*]').getOrCreate()  
```

# Loading data into pySpark

```python
from pyspack.sql.types import StructType, StrucktFeild, IntergerType, StringType, DateType

# Schema typing:
schema = StructType([
    StructField('id', IntegerType(), True),
    StruckField('name', StringType(), True),
    StructField('sale_date', DateType(), True)

])

# for a date of "11/12/2025 12:40:15"   we would need to transform the data to Datetype so we use UTC time.


df_from_csv = spark.read.csv('file.csv', schema=schema, header=True)
df_from_parquet = spark.read.parquet('file.parquet')
df_from_json = spark.read.json('file.json')




```

#  Nulls

```python
df_sparc.dropna(how='any')   #  Remove any record with a field == null
df_sparc.dropna(subset=['colA', 'colD'])   # If fields in Columns A or D have Nulls , drop the row.


df_sparc.fillna(value=0)  # replace all null values with the value 0
df_sparc.fillna(value=0, subset=['colA', 'colD'] ) # for numbered column types
df_sparc.fillna(value='notavalue', subset=['colA', 'colD'] ) # for string column types


# or Impute values 
# no example
```

# Joins
## Narrow
 i think this is where we extract output from inside the partition.  using map(), filter() 

## Wide
This is where we join two or more  partitions  to make an output using  groupBy(), join(), sotBy()

## Catalyst
An optimiser  in Spark using rules to optimise the query performance. transforms and improves user SQL to create a more efficient execution plan.

```python

df_sparc.join( df_from_another_dataset, on='id', how='inner')  # Inner join on matching colunn id in both dataframes
df_sparc.join( df_from_another_dataset, on='id', how='outer')  # add matching rows where 'id' in df_from_another_dataset, to df_sparc. Return expanded dataframe. 


```
# transform column
```python

def get_discount_price(df):
    return df.withColumn('discounted_price', df.price -  (df.price * df.discount) /100)

df_discounted = df_spark.transform(get_discount_price)

```

# SQL
```python

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

window = Window.orderBy('disconted_price')

df_results = df_spark/withColumn('row_number', row_number().over(window)) 
```

# Memory
```python

# Cache data in memory
df_sparc.cache()   

# Persist data to local disk
df_sparc.persist(storageLevel=StorageLevel.DISK_ONLY)

# other level
# MEMORY_ONLY - keeps in ram
# MEMORY_AND_DISK - keeps in ram if paoosible, spills to disk
# DISK_ONLY - stores on disk - safe for large data sets
# MEMORY_ONLY_SER - stores serialized objects in memory.

```

# Processing
 - RDD - Resilient Distributed Datasets. Low level Spark collections of data
 - Dataframe - high level API built on top of RDD, they organise and structure into columns
 - Dataset = combine the benefits of RDD and Dataframes and provide compile time checking - No idea what this meand - need to learn more about this.

 - Lazy Evaluation:
 pysparck implements lazy evaluation, meaning transformation are not executed immediatly. Spark builds a sequence of operations called a DAG  (directed acrylic graph). Optimisation of exeution is deffered until the action is triggered.  

 - Partioning
We want to distribute execution evenly accross nodes in a cluster. Partitioning is controlled by .repartition() and .coalesce(). 
Aim for 2 - 4 partition per core.

Before partitioning work out the  balance of partions to avoid skew.

For small dataset - don't bother repartioning.

Having completed work, and now you want to write to parquet:  Then lots of partiotion may create lots of parquet files.  So coalesce is usefull to reduce the number of files.

```python
df_repartition = df_spark.reparition(16, 'id')  #   create 16 partions of df_spark, based on column 'id'.
```
## Checkpoints
Checkpointing save the rdd to disk  as an intermediate point, providing a way to recover from failed states.

# Broadcast
Broadcast variable are applied to all partitions,  they need to be a very small dataset.

# Spark Driver
this is the core process the orchestrates spark application by executing task acros the clusters. 
It communicates with cluster manager to:
- allocate resource, 
- schedule task,
- monitor execution

Cluster Mangers:
- Standalone, simple cluster inside spark
- Hadoop YARM - job scheduling and resource management
- Kubernetes - Container orchestration
- Apache Mesos - ?  distributed system for managing resource per application.


# Spark DAG
Directed acrylic graph: is a entity that represents the logical execution model. Each node represents a transfomation executed in a specific order. The plan is optimised for transformation, task coalescing and predicate pushdown.
For example: 
```json
{ 
    "dag": { 
        "nodes": [ 
            { "id": "1", "name": "JSON_READ", "type": "source" }, 
            { "id": "2", "name": "FILTER", "type": "transformation" }, 
            { "id": "3", "name": "MAP_1", "type": "transformation" }, 
            { "id": "4", "name": "MAP_2", "type": "transformation" }, 
            { "id": "5", "name": "JOIN", "type": "transformation" }, 
            { "id": "6", "name": "AGGREGATE", "type": "transformation" }, 
            { "id": "7", "name": "SORT", "type": "transformation" }, 
            { "id": "8", "name": "PARQUET_WRITE", "type": "action" } 
        ], 
        "edges": [ 
            { "from": "1", "to": "2" }, 
            { "from": "2", "to": "3" }, 
            { "from": "2", "to": "4" }, 
            { "from": "3", "to": "5" }, 
            { "from": "4", "to": "5" }, 
            { "from": "5", "to": "6" }, 
            { "from": "6", "to": "7" }, 
            { "from": "7", "to": "8" } 
        ] 
    } 
}
```

# Error Handling:
Usual python try and exception:
```python
try:
    # some code

except Exception as e:
    # handler
    logger.error(type(e).__name__, exc_info=True )
    logger.error(str(e), exc_info=True )

logger.info('Python script finished')

``` 