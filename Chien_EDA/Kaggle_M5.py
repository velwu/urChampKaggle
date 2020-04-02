import pandas as pd
import numpy as np

price = pd.read_csv('data/sell_prices.csv')
price_CA1 = price[price['store_id'] == 'CA_1']
price_CA2 = price[price['store_id'] == 'CA_2']
price_CA3 = price[price['store_id'] == 'CA_3']
calendar = pd.read_csv('data/calendar.csv')
calendar_train = calendar[:1913]
sale = pd.read_csv('data/sales_train_validation.csv')
sale_CA1 = sale[sale['store_id'] == 'CA_1']


# Analysis on event during training period (d_1 ~ d_1913)
event1 = calendar_train[['event_name_1', 'event_type_1']].dropna()
event2 = calendar_train[['event_name_2', 'event_type_2']].dropna()
ttl_event = pd.concat([event1.rename(columns={'event_name_1': 'event_name', 'event_type_1': 'event_type'}),
                       event2.rename(columns={'event_name_2': 'event_name', 'event_type_2': 'event_type'})])
print("There are", event1['event_name_1'].nunique(), "unique event_1,", event2['event_name_2'].nunique(),
      "unique event_2, and", ttl_event['event_name'].nunique(), "total unique event in the training period.")
print("There are", event1.shape[0], "days have event_1, and", event2.shape[0],
      "days have event2 while", calendar_train.shape[0] - event1.shape[0], "days do not have any event.")
ttl_event.groupby('event_type').size()

# Find how many days which SNAP purchases are allowed in the three states
print("There are totally", sum(calendar['snap_CA'] == 1), "days where SNAP purchases are allowed in CA.")
print("There are totally", sum(calendar['snap_TX'] == 1), "days where SNAP purchases are allowed in TX.")
print("There are totally", sum(calendar['snap_WI'] == 1), "days where SNAP purchases are allowed in WI.")

# Find the dates on which SNAP purchases are allowed in the three states
snap_date_CA = calendar[calendar['snap_CA'] == 1]['date'].str[-2:]
snap_date_CA.value_counts().sort_index()

snap_date_TX = calendar[calendar['snap_TX'] == 1]['date'].str[-2:]
snap_date_TX.value_counts().sort_index()

snap_date_WI = calendar[calendar['snap_WI'] == 1]['date'].str[-2:]
snap_date_WI.value_counts().sort_index()

# Find missing values in price
# Find the weeks that the weekly avg. price is missing for each item in the CA1 store
price_missing = {}
unq_wm_wk = set(calendar['wm_yr_wk'].unique())
for item in price_CA1['item_id'].unique():
    missing_wk = list(unq_wm_wk - set(price_CA1[price_CA1['item_id'] == item]['wm_yr_wk'].unique()))
    if len(missing_wk) > 0:
        price_missing[item] = missing_wk
# (to be continued)Replace missing weekly avg. prices with the prices of the same item for the same week in other stores
replace_price = pd.Dataframe(columns=['item_id', 'sell_price'])
for k in price_missing.keys():
    for v in price_missing[k]:
        if price_CA2[(price_CA2['item_id'] == k) & (price_CA2['w'] == v)]['sell_price'].empty:




# Transpose 'd_1' to 'd_1913' columns of 'sale' and join the result with 'calendar'
sale_colname = sale.columns
sale_CA1 = pd.melt(sale[sale['store_id'] == 'CA_1'], id_vars=sale_colname[1:6],
                   value_vars=sale_colname[6:], var_name='d', value_name='sales')
sale_CA1_h = sale_CA1.head(30492)
CA1 = pd.merge(sale_CA1, calendar, how='left', on='d')