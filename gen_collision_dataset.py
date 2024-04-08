import pandas as pd
import argparse
import csv
from datetime import datetime

pd.options.mode.chained_assignment = None

def generate_association_rules(raw_df):
    raw_df['transactions'] = raw_df['ZIP CODE'].astype(str) + ',' + raw_df['VEHICLE TYPE CODE 1'].astype(str) + ',' + raw_df['VEHICLE TYPE CODE 2'].astype(str)
    # raw_df['transactions'] = raw_df['CONTRIBUTING FACTOR VEHICLE 1'].astype(str) + ',' + raw_df['VEHICLE TYPE CODE 1'].astype(str)
    
    raw_df['CRASH DATE'] = pd.to_datetime(raw_df['CRASH DATE'])
    raw_df.dropna(subset=['ZIP CODE'], inplace=True)
    raw_df['ZIP CODE'] = raw_df['ZIP CODE'].astype(str)

    raw_df = raw_df[raw_df['CRASH DATE'] > datetime(2023, 1, 1)]
    transactions_ls = []
    for b in raw_df['transactions'].unique():
        items = b
        items+=','
        # print('TYPE: ', raw_df[raw_df['transactions'] == b]['CONTRIBUTING FACTOR VEHICLE 1'])
        items+=','.join(list(raw_df[raw_df['transactions'] == b]['ZIP CODE'].dropna().str.strip().unique()))
        # items+=','.join(list(raw_df[raw_df['transactions'] == b]['CONTRIBUTING FACTOR VEHICLE 1'].dropna().str.strip().unique()))
        if len(items) > 0:
            transactions_ls += [items]

    out_df = pd.DataFrame(transactions_ls).dropna()
    return out_df

def generate_association_rules_alt(raw_df):
    raw_df['transactions'] =  raw_df['CONTRIBUTING FACTOR VEHICLE 1'].astype(str) + ',' +  raw_df['CONTRIBUTING FACTOR VEHICLE 1'].astype(str)  
    # raw_df['transactions'] = raw_df['CONTRIBUTING FACTOR VEHICLE 1'].astype(str) + ',' + raw_df['VEHICLE TYPE CODE 1'].astype(str)
    
    raw_df['CRASH DATE'] = pd.to_datetime(raw_df['CRASH DATE'])
    raw_df = raw_df[raw_df['CRASH DATE'] > datetime(2023, 1, 1)]
    raw_df.dropna(subset=['ZIP CODE'], inplace=True)
    raw_df['ZIP CODE'] = raw_df['ZIP CODE'].astype(str)

    raw_df['NUMBER OF PERSONS INJURED'] = raw_df['NUMBER OF PERSONS INJURED'].astype(str)
   
    transactions_ls = []
    for b in raw_df['transactions'].unique():
        items = b
        items+=','
        # print('TYPE: ', raw_df[raw_df['transactions'] == b]['CONTRIBUTING FACTOR VEHICLE 1'])
        items+=','.join(list(raw_df[raw_df['transactions'] == b]['NUMBER OF PERSONS INJURED'].dropna().str.strip().unique()))
        # items+=','.join(list(raw_df[raw_df['transactions'] == b]['CONTRIBUTING FACTOR VEHICLE 1'].dropna().str.strip().unique()))
        if len(items) > 0:
            transactions_ls += [items]

    out_df = pd.DataFrame(transactions_ls).dropna()
    return out_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate association rules from raw data')
    parser.add_argument('raw_df', type=str, help='Path to the raw data file')
    parser.add_argument('out_df', type=str, help='Path to the output dataframe file')

    args = parser.parse_args()

    # Read raw data from input file
    raw_df = pd.read_csv(args.raw_df)

    # Generate association rules
    out_df = generate_association_rules_alt(raw_df)

    # Write output dataframe to file
    f = open(args.out_df, "w")
    for v in out_df.values:
        f.write("{}\n".format(v[0]))