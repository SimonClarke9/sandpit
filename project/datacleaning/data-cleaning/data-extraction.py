from pathlib import  Path
import polars as pl



# Input CSV
csv_path = "crime_incidents_messy.csv"

# Output directory
output_dir = Path("crime")
output_dir.mkdir(exist_ok=True)

# Read CSV lazily (best for large files)
df = pl.read_csv(csv_path)

#let clean the data 
#Lowercase all string columns except those containing "_id"
string_cols =[
    col
    for col, dtype in  df.schema.items()
    if dtype == pl.Utf8 and "_id" not in col
    ]

df = df.with_columns([
    pl.col(col).str.to_lowercase().alias(col)
    for col in string_cols
    ])

# Uppercase all columns with string type and including "_id"
string_cols =[
    col
    for col, dtype in  df.schema.items()
    if dtype == pl.Utf8 and "_id" in col
    ]

df = df.with_columns([
    pl.col(col).str.to_uppercase().alias(col)
    for col in string_cols
    ])


# create new dataframe with unique values for each column.
restricted_cold = ["address", "incident_datetime"]
string_cols = [
    col
    for col, dtype in df.schema.items()
    if dtype == pl.Utf8 and "_id" not in col and col not in restricted_cold ]

df = df.with_columns([
    pl.col(col).str.strip().alias(col)
    for col in string_cols
])


unique_cols = pl.concat([
    df[col]
        .unique()
        .sort()
        .drop_nulls()
        .to_frame(name="value")
        .with_columns(pl.lit(col).alias("column_name"))
    for col in string_cols
])
# Reorder columns
unique_cols = unique_cols.select(["column_name", "value"])

unique_cols.write_csv(output_dir / "lookups.csv")


head = df.head()
print(head)

exit
# Partition columns
partition_cols = ["state", "crime_type"]

# Group by partitions
for keys, group in df.group_by(partition_cols):
    state, crime = keys
    state = state.strip()
    crime = crime.strip()

    # Build directory structure
    part_path = output_dir / f"state={state}" / f"crime_type={crime}"
    part_path.mkdir(parents=True, exist_ok=True)

    # Write parquet file
    group.write_parquet(part_path / "data.parquet")