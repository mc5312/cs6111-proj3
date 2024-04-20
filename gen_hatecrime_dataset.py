import pandas as pd
import argparse
import re

def clean_str(s):
    """
    Util function for cleaning string in raw data
    """
    clean = re.sub('[^a-zA-Z]+', ' ', s)
    clean = re.sub('[\s]+', '_', clean.strip())
    if clean == 'YRS_AND_OLDER': clean = 'SIXTY_YRS_AND_OLDER'
    return clean

def generate_transactions(raw_csv_path, items):
    """
    Read csv in input path. Generate transactions in list format.
    Transaction basket is defined by: 'Complaint Year Number', 'Month Number', 'Complaint Precinct Code'
    """
    raw_df = pd.read_csv(raw_csv_path)
    raw_df['transaction_id'] = raw_df[['Complaint Year Number', 'Month Number', 'Complaint Precinct Code']].apply(
        lambda x: '|'.join([str(c) for c in x]), axis=1
    )
    raw_df = raw_df[['transaction_id'] + items]

    for item in items:
        raw_df[item] = raw_df[item].apply(lambda x: clean_str(x))

    transactions = []
    for t in raw_df['transaction_id'].unique():
        itemset = []
        for item in items:
            itemset += list(raw_df[raw_df['transaction_id'] == t][item].unique())
        itemset = ','.join(itemset)
        if len(itemset) > 0:
            transactions += [itemset]

    return transactions

def output_dataset(output_csv_path, transactions):
    """
    Output transactions list to csv.
    """
    with open(output_csv_path, "w") as f:
        for t in transactions:
            f.write("{}\n".format(t))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Transaction Dataset')
    parser.add_argument('raw_csv_path', type=str, help='Path to the raw csv file')
    parser.add_argument('output_csv_path', type=str, help='Path to the output csv file')
    args = parser.parse_args()

    # Potential item columns:
    #     'Law Code Category Description', 'Offense Description', 'PD Code Description', 'Bias Motive Description', 'Offense Category'
    # Selected item columns:
    items = ['Offense Description', 'Bias Motive Description']

    transactions_ls = generate_transactions(args.raw_csv_path, items)
    output_dataset(args.output_csv_path, transactions_ls)