import pandas as pd
import csv

raw_df = pd.read_csv("2015_Street_Tree_Census_-_Tree_Data.csv")
raw_df = raw_df[['spc_common', 'borough', 'nta_name', 'zip_city', 'user_type', 'status', 'health']]
raw_df = raw_df.dropna()

# print(len(raw_df))
raw_df['spc_common'] = raw_df['spc_common'].apply(lambda x: x.replace(',', '&').replace(' ', ''))
raw_df['transactions'] = raw_df['borough'] + raw_df['nta_name'] + raw_df['zip_city'] + raw_df['user_type'] + raw_df['status'] +  raw_df['health']

transactions_ls = []
for b in raw_df['transactions'].unique():
    items = ','.join(list(raw_df[raw_df['transactions'] == b]['spc_common'].str.strip().unique()))
    if len(items) > 0:
        transactions_ls += [items]

out_df = pd.DataFrame(transactions_ls).dropna()

print(len(out_df), max([len(x.split(',')) for x in transactions_ls]))

# f = open('INTEGRATED-DATASET.csv', "w")
# for v in out_df.values:
#     f.write("{}\n".format(v[0]))
# f.close()