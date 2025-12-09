Core Concepts
ANSI SQL compliant: Trino supports standard SQL syntax with extensions for distributed queries.

Connectors: Query across multiple data sources (Hive, Iceberg, Delta Lake, MySQL, PostgreSQL, etc.).

Schemas & Catalogs: Organize data sources → catalog.schema.table.

## Basic Commands
```sql
-- Create a table
CREATE TABLE catalog.schema.table (
    id INT,
    name VARCHAR,
    created_at TIMESTAMP
);


-- Insert data
INSERT INTO catalog.schema.table (id, name) VALUES (1, 'Alice');

-- Select data
SELECT id, name FROM catalog.schema.table WHERE id = 1;

-- Drop table
DROP TABLE catalog.schema.table;
```
## Querying Data
```sql
-- Filtering
SELECT * FROM orders WHERE order_date >= DATE '2025-01-01';

-- Aggregation
SELECT customer_id, SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;

-- Joins
SELECT o.id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id;

-- Window functions
SELECT customer_id, SUM(amount) OVER (PARTITION BY customer_id) AS total_spent
FROM orders;
```

## Functions & Operators
String: CONCAT(), SUBSTRING(), LOWER(), UPPER(), TRIM()

Date/Time: CURRENT_DATE, CURRENT_TIMESTAMP, DATE_ADD(), DATE_DIFF()

Math: ABS(), ROUND(), CEIL(), FLOOR(), POWER()

Conditional: CASE WHEN ... THEN ... ELSE ... END

## Advanced Features
CTEs (Common Table Expressions)

```sql
WITH top_customers AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT * FROM top_customers WHERE total_spent > 1000;
```
Materialized Views
```sql
CREATE MATERIALIZED VIEW top_orders AS
SELECT * FROM orders WHERE amount > 500;
```
Explain Plan

```sql
EXPLAIN SELECT * FROM orders WHERE amount > 100;
```
## Quick Reference Table
Category	Syntax Example
Create Table	CREATE TABLE schema.table (...)
Insert Data	INSERT INTO table VALUES (...)
Select Data	SELECT col FROM table WHERE ...
Joins	SELECT ... FROM A JOIN B ON ...
Aggregation	SELECT SUM(col) FROM table GROUP BY ...
Window Funcs	SUM(col) OVER (PARTITION BY ...)
Drop Table	DROP TABLE schema.table
Sources: Official Trino SQL syntax docs, GitHub Trino cheat sheet, and Trino language reference (3).


## Table Creation
```sql
-- Create an Iceberg catalog
CREATE CATALOG iceberg_catalog
WITH (catalog_type='iceberg',
      warehouse='s3://your-bucket/warehouse/');

-- Create an Iceberg table
CREATE TABLE iceberg_catalog.db.orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date DATE,
    amount DOUBLE
)
WITH (format='ICEBERG');
```
## Querying
```sql
-- Basic query
SELECT customer_id, SUM(amount) AS total_spent
FROM iceberg_catalog.db.orders
WHERE order_date >= DATE '2025-01-01'
GROUP BY customer_id
ORDER BY total_spent DESC;

-- Time travel (query past snapshot)
SELECT * FROM iceberg_catalog.db.orders
FOR TIMESTAMP AS OF TIMESTAMP '2025-12-01 00:00:00';
```
## Insert
```sql
-- Insert new rows
INSERT INTO iceberg_catalog.db.orders (order_id, customer_id, order_date, amount)
VALUES (101, 2001, DATE '2025-12-01', 500.00);
```
## Update
```sql
-- Update existing rows
UPDATE iceberg_catalog.db.orders
SET amount = amount * 1.1
WHERE order_date = DATE '2025-12-01';
```
## Delete
```sql
-- Delete rows
DELETE FROM iceberg_catalog.db.orders
WHERE order_date < DATE '2025-01-01';
```

## Merge (Upsert)
```sql
MERGE INTO iceberg_catalog.db.orders AS target
USING iceberg_catalog.db.staging_orders AS source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET amount = source.amount
WHEN NOT MATCHED THEN INSERT (order_id, customer_id, order_date, amount)
VALUES (source.order_id, source.customer_id, source.order_date, source.amount);
```
## Key Notes
Athena uses Iceberg v2 row-level deletes/updates with merge-on-read semantics.

Each INSERT, UPDATE, DELETE creates a new snapshot, enabling time travel queries.

Copy-on-write settings are ignored; Athena enforces merge-on-read.

**Ensure Athena Engine v3 or later for full Iceberg support.**

## Quick Reference Table
Operation	Syntax Example
Create	CREATE TABLE ... WITH (format='ICEBERG')
Query	SELECT ... FROM table
Insert	INSERT INTO table VALUES (...)
Update	UPDATE table SET ... WHERE ...
Delete	DELETE FROM table WHERE ...
Merge	MERGE INTO table USING source ...
Time Travel	SELECT ... FOR TIMESTAMP AS OF ...