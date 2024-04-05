import pandas as pd
import csv

raw_df = pd.read_csv("Good_Food_Purchasing_Data.csv")

raw_df['Food Product Category'] = raw_df['Food Product Category'].apply(lambda x: x.replace(',', '&').replace(' ', ''))
raw_df['transactions'] = raw_df['Time Period'] + ':' + raw_df['Agency'] + ':' + raw_df['Distributor']

transactions_ls = []
for b in raw_df['transactions'].unique():
    items = ','.join(list(raw_df[raw_df['transactions'] == b]['Food Product Category'].str.strip().unique()))
    if len(items) > 0:
        transactions_ls += [items]

out_df = pd.DataFrame(transactions_ls).dropna()
f = open('INTEGRATED-DATASET.csv', "w")
for v in out_df.values:
    f.write("{}\n".format(v[0]))
f.close()
