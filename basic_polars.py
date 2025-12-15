import polars as pl
import sys


def main():    # Create a simple DataFrame
    sys.stdout.flush()
    data_path = 'data_csv.csv'   
    df = pl.read_csv(data_path)

   # Display the DataFrame
    print("DataFrame:")
    print(df)

    df = pl.read_json('nested_json.json')

    df_exploded = (df.explode('items').unnest('items').unnest('customer'))

   # Display the DataFrame
    print("DataFrame:")
    print(df)

    print("Df Exploded:")
    print(df_exploded)


if __name__ == "__main__":
    main()
