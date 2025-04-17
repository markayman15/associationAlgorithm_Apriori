import pandas as pd
from collections import Counter

def transform_data(path, precentage):
    transactions_items = pd.read_csv(path)

    count = transactions_items.shape[0]

    #transactions_items = transactions_items.iloc[:int(count * (precentage / 100))]

    #dis_items = transactions_items['itemDescription'].value_counts()

    grouped_transaction_items = transactions_items.groupby(['Member_number', 'Date']).agg({'itemDescription':','.join})
    grouped_transaction_items['item_set'] = grouped_transaction_items['itemDescription'].str.split(",").apply(set)

    grouped_transaction_items = grouped_transaction_items.iloc[:int(count * (precentage / 100))]

    #all_items = [item for item_set in grouped_transaction_items['item_set'] for item in item_set]
    all_items = []
    for itemset in grouped_transaction_items['item_set']:
        for item in itemset:
            all_items.append(item)
    dis_items = Counter(all_items)
    dis_items = pd.Series(dis_items).sort_values(ascending=False)


    return grouped_transaction_items, dis_items,count