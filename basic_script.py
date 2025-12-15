import pandas as pd
import sys
from datetime import datetime



def parse_mixed_date(date_str):
    """
    Expand two digit year to four digit year.
    return datestring as datetime type
    
    :param date_str: Description
    """
    date_str= date_str.strip()
    day, month, year = date_str.split('/')
    if len(year) != 4 :
        if int(year) >= 50:
            year= '19' + year
            date_str = f"{day}/{month}/{year}"  

    if int(month) > 12 : # must be USA format
        return datetime.strptime(date_str, "%m/%d/%Y")
    else:              # assume US format
        return datetime.strptime(date_str, "%d/%m/%Y")
    


def main():    # Create a simple DataFrame
    sys.stdout.flush()

    # data = {
    #     'Name': ['Alice', 'Bob', 'Charlie'],
    #     'Age': [25, 30, 35],
    #     'City': ['New York', 'Los Angeles', 'Chicago']
    # }
    data_path = 'data_csv.csv'
    df = pd.read_csv(data_path)

    # Display the DataFrame
    print("DataFrame:")
    print(df)

    #data quality processing
    # convert string to lower case.
    cols = ['forename', 'surname', 'country']
    df[cols] = df[cols].apply(lambda x: x.str.lower())

    # convert dob to datetime 
    df['dob'] = df['dob'].apply(parse_mixed_date)
    df['dob'] = pd.to_datetime(df['dob']).dt.tz_localize('UTC')
    # df['dob'] = pd.to_datetime(df['dob'])  # this convert 71 to 2071 

    # drop duplicates
    df = df.drop_duplicates()
    



   # Display the DataFrame
    print("DataFrame:")
    print(df)

    # # Calculate the average age
    # average_age =     ['Age'].mean()
    # print(f"\nAverage Age: {average_age}")  

if __name__ == "__main__":
    main()
