import pandas as pd
import argparse
import csv

def generate_association_rules(raw_df):
    raw_df = raw_df.drop(columns=['Full Complaint ID', 'Arrest Id'])
    # raw_df['Bias Motive Description'] = raw_df['Food Product Category'].apply(lambda x: x.replace(',', '&').replace(' ', ''))
    #raw_df['transactions'] = raw_df['Complaint Year Number']+ ':' + raw_df['Month Number'] + ':' + raw_df['Complaint Precinct Code']
    raw_df['Bias Motive Description'] = raw_df['Bias Motive Description'].apply(lambda x: x.replace(',', '&').replace(' ', '')) 
    raw_df['PD Code Description'] = raw_df['PD Code Description'].apply(lambda x: x.replace(',', '-').replace(' ', ''))
    # raw_df['transactions'] = raw_df['Complaint Year Number'].astype(str) +  ',' + raw_df['Month Number'].astype(str) + ',' + raw_df['Patrol Borough Name'].astype(str) + ',' 
    # + raw_df['PD Code Description'].astype(str)

    raw_df['transactions'] = raw_df['Complaint Year Number'].astype(str) +  ',' + raw_df['Month Number'].astype(str) + ',' + raw_df['Complaint Precinct Code'].astype(str)
    # print(raw_df['transactions'])

    transactions_ls = []
    for b in raw_df['transactions'].unique():
        offense_desc = raw_df[raw_df['transactions'] == b]['Offense Description'].str.strip().unique()
        bias_desc = raw_df[raw_df['transactions'] == b]['Bias Motive Description'].str.strip().unique()
        combined_desc = list(offense_desc) + list(bias_desc)
        items = ','.join(combined_desc)
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