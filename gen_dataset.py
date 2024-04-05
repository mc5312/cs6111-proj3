import pandas as pd

raw_df = pd.read_csv("Good_Food_Purchasing_Data.csv")

raw_df['Food Product Category'] = raw_df['Food Product Category'].apply(lambda x: x.replace(',', '&').replace(' ', ''))
raw_df['transactions'] = raw_df['Time Period'] + ':' + raw_df['Agency'] + ':' + raw_df['Distributor']

transactions_ls = []
for b in raw_df['transactions'].unique():
    items = ','.join(list(raw_df[raw_df['transactions'] == b]['Food Product Category'].str.strip().unique()))
    if len(items) > 0:
        transactions_ls += [items]

out_df = pd.DataFrame(transactions_ls).dropna()
out_df.to_csv('INTEGRATED-DATASET.csv', index=False, header=False)
