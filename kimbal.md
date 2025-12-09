# Core Concepts
Dimensional Modeling: Organizes data into facts (measurable events) and dimensions (context for those facts).

Star Schema: Central fact table surrounded by dimension tables. Simple, denormalized, and optimized for queries.

Grain: Defines the level of detail in a fact table (e.g., “one row per sales transaction”).

## Design Process (Kimball Four-Step)
Select the Business Process

Identify the subject area (sales, inventory, orders).

Declare the Grain

Decide what a single fact table row represents.

Identify the Dimensions

Who, what, where, when, why, and how.

Identify the Facts

Numeric measures (sales amount, quantity, cost).

## Fact Tables
Types of Facts:

Additive: Can be summed across dimensions (sales amount).

Semi-additive: Summed across some dimensions (account balance).

Non-additive: Cannot be summed (ratios, percentages).

Snapshots:

Transaction Fact Table: Each event recorded.

Periodic Snapshot: Regular intervals (daily sales totals).

Accumulating Snapshot: Tracks progress of a process (order fulfillment).

## Dimension Tables
Characteristics:

Wide, denormalized, descriptive attributes.

Use surrogate keys instead of natural keys.

Types of Dimensions:

Conformed Dimensions: Shared across fact tables (e.g., Date, Customer).

Slowly Changing Dimensions (SCD): Handle attribute changes over time.

Type 0: Retain Original – Attributes will never change.
Type 1: Overwrite – Overwrite an attribute if it has changed, reflecting the most recent version of the record.
Type 2: Add New Row – Expire previous row and add a new row with the new information. Set as the current record.
Type 3: Add New Attribute – Move old attribute value into the “old_value” column and update the main value column with incoming value.
Type 4: Add Mini-Dimension – When a group of attributes in a dimension are rapidly changing is split into it’s own dimension; aka Rapidly Changing Monster Dimension.
Type 5: Add Mini-Dimension and Type 1 Outrigger – Preserve historical attribute values and report historical facts according to current attributes.
Type 6: Add Type 1 Attributes to Type 2 Dimension
Type 7: Dual Type 1 and Type 2 Dimension – Support as-was and as-is reporting

## Best Practices
Resist normalization—denormalize for query speed.

Avoid cryptic abbreviations; use meaningful names.

Handle NULLs carefully (missing or unknown values).

Ensure consistency with conformed dimensions across the warehouse.

## Quick Reference Table
Step	Focus	Example
1. Business Process	Subject area	Sales transactions
2. Grain	Row definition	One row per sale
3. Dimensions	Context	Customer, Product, Date
4. Facts	Measures	Quantity, Revenue
In short: Kimball’s dimensional modeling is about building intuitive, query-friendly star schemas with clear grains, well-defined fact tables, and descriptive dimension tables. It prioritizes usability and performance over strict normalization


## Surrogate Keys (Kimball Approach)
Definition: A surrogate key is a meaningless, sequential integer used as the primary key in dimension tables.

Why Use Them:

Natural keys may change over time or differ across source systems.

Surrogate keys ensure stability, uniqueness, and independence from operational systems.

How to Create
Use an auto-increment integer (e.g., IDENTITY in SQL Server, SEQUENCE in Oracle/Postgres).

Assign a new surrogate key whenever a new dimension row is inserted.

Never expose surrogate keys outside the warehouse—they are internal identifiers only.

Example (SQL)
sql
'''SQL
CREATE TABLE Customer_Dim (
    Customer_Key INT IDENTITY(1,1) PRIMARY KEY,
    Customer_Natural_Key VARCHAR(50),
    Customer_Name VARCHAR(100),
    Customer_Type VARCHAR(50),
    Effective_Date DATE,
    Expiry_Date DATE
);
'''

## Salted Keys (Hashed Surrogate Keys)
Definition: A salted key is a hash-based surrogate key created by combining multiple attributes with a random or fixed “salt” string to avoid collisions.

Why Use Them:

Useful when building surrogate keys from composite natural keys.

Prevents duplicate hashes when values are similar.

Ensures repeatability and uniqueness across distributed systems.

How to Create
Concatenate natural key attributes + salt.

Apply a hashing function (MD5, SHA-256).

Store as a fixed-length string or integer.

Example (SQL)
sql
-- Salted surrogate key using SHA2
SELECT 
    CAST(HASHBYTES('SHA2_256', CONCAT(Customer_ID, '|', Region, '|', 'SALT123')) AS VARBINARY(32)) AS Surrogate_Key,
    Customer_ID,
    Region,
    Other_Attributes
FROM Staging_Customer;

## Quick Reference Table
Technique	Purpose	Pros	Cons	Example
Surrogate Key	Stable internal PK	Simple, fast, independent	Requires sequence management	Auto-increment integer
Salted Key	Hash-based PK	Avoids collisions, repeatable	Longer, less human-readable	SHA-256 hash with salt

## Key Considerations
Surrogate keys are Kimball’s recommended default for dimension tables.

Salted keys are more common in modern cloud warehouses (Snowflake, BigQuery, dbt) where hashing is efficient.

Always ensure consistency: surrogate keys must be unique and immutable.

Salt values should be fixed and documented to guarantee reproducibility.



