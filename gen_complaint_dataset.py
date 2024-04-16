from datetime import datetime
import pandas as pd
import argparse

def generate_association_rules(raw_df):    
    raw_df['CMPLNT_FR_DT'] = pd.to_datetime(raw_df['CMPLNT_FR_DT'], errors='coerce')
    raw_df['CMPLNT_FR_YR'] =  raw_df['CMPLNT_FR_DT'].dt.year

    raw_df['transactions'] = raw_df['CMPLNT_FR_YR'].astype(str) + ',' + raw_df['ADDR_PCT_CD'].astype(str) 

    transactions_ls = []
    for b in raw_df['transactions'].unique():
        items = ','.join(list(raw_df[raw_df['transactions'] == b]['OFNS_DESC'].dropna().str.strip().unique()))
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
    out_df = generate_association_rules(raw_df)

    # Write output dataframe to file
    f = open(args.out_df, "w")
    for v in out_df.values:
        f.write("{}\n".format(v[0]))