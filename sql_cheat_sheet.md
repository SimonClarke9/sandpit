#SQL Interview Cheat Sheet

## Core Concepts

SQL (Structured Query Language): Used to interact with relational databases.

Types of SQL commands:

DDL (Data Definition Language): CREATE, ALTER, DROP

DML (Data Manipulation Language): INSERT, UPDATE, DELETE

DQL (Data Query Language): SELECT

DCL (Data Control Language): GRANT, REVOKE

TCL (Transaction Control Language): COMMIT, ROLLBACK, SAVEPOINT

## Common Queries

Select data:

```SQL
SELECT column1, column2 FROM table WHERE condition;

Insert data:

INSERT INTO table (col1, col2) VALUES ('val1', 'val2');

Update data:

UPDATE table SET col1 = 'newVal' WHERE condition;

Delete data:

DELETE FROM table WHERE condition;
```

## Joins

```SQL
INNER JOIN: Returns matching rows.

LEFT JOIN: All rows from left + matches from right.

RIGHT JOIN: All rows from right + matches from left.

FULL OUTER JOIN: All rows from both tables.

CROSS JOIN: Cartesian product.
```

Example:

'''SQL
SELECT a.name, b.department
FROM employees a
INNER JOIN departments b ON a.dept_id = b.id;
'''

## Aggregations

Functions: COUNT(), SUM(), AVG(), MIN(), MAX()

GROUP BY:

''SQL
SELECT dept_id, COUNT(*) 
FROM employees 
GROUP BY dept_id;
''

HAVING: Filters groups after aggregation.

'''SQL
SELECT dept_id, COUNT(*) 
FROM employees 
GROUP BY dept_id
HAVING COUNT(*) > 5;
'''


## Subqueries

Single-row subquery:

'''SQL
SELECT name FROM employees WHERE salary = (SELECT MAX(salary) FROM employees);
'''

Multi-row subquery:

'''SQL
SELECT name FROM employees WHERE dept_id IN (SELECT id FROM departments WHERE location='NY');
'''

## Indexes & Keys

Primary Key: Unique + not null.

Foreign Key: References another table.

Unique Key: Ensures uniqueness.

Index: Speeds up queries but increases write cost.

## Transactions

ACID properties: Atomicity, Consistency, Isolation, Durability.

Commands:

'''SQL
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id=1;
UPDATE accounts SET balance = balance + 100 WHERE id=2;
COMMIT;
'''

## Window Functions

Window functions perform calculations across a set of rows related to the current row, without collapsing results like GROUP BY.

Syntax

'''SQL
function_name(column) OVER (
    PARTITION BY col1
    ORDER BY col2
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
'''

Common Window Functions

ROW_NUMBER() → Sequential number per partition

RANK() → Ranking with gaps for ties

DENSE_RANK() → Ranking without gaps

NTILE(n) → Distributes rows into n buckets

LEAD() → Value from next row

LAG() → Value from previous row

SUM() / AVG() → Running totals or moving averages

Examples

Ranking Employees by Salary:

''SQL
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;
'''

Running Total of Sales:

'''SQL
SELECT month, sales,
       SUM(sales) OVER (ORDER BY month) AS running_total
FROM revenue;
''' 

Compare Current vs Previous Salary:


'''SQL
SELECT name, salary,
       LAG(salary) OVER (ORDER BY hire_date) AS prev_salary
FROM employees;
'''

## Advanced Topics

CTEs (Common Table Expressions):

'''SQL
WITH dept_count AS (
  SELECT dept_id, COUNT(*) AS cnt FROM employees GROUP BY dept_id
)
SELECT * FROM dept_count WHERE cnt > 5;
'''

Normalization: Organizing data to reduce redundancy.

Denormalization: Adding redundancy for performance.

## Typical Interview Questions

Difference between WHERE vs HAVING

Difference between INNER JOIN vs LEFT JOIN

What are indexes and when to use them?

Explain normalization forms (1NF, 2NF, 3NF, BCNF)

How do transactions ensure consistency?

Difference between DELETE, TRUNCATE, and DROP

How do window functions differ from GROUP BY?