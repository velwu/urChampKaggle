# pip install matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

csv_calendar = pd.read_csv("calendar.csv")
csv_SellPrices = pd.read_csv("sell_prices.csv")
csv_TrainValidation = pd.read_csv("sales_train_validation.csv")

# Preprocessing: FOOD category
event_1 = pd.DataFrame(csv_calendar.iloc[:, 7:9].values, columns = ['Name', 'Type'])
event_2 = pd.DataFrame(csv_calendar.iloc[:, 9:11].values, columns = ['Name', 'Type'])

# Missing value: NaN = 0
event_1 = event_1.fillna(0).astype('str')   # LabelEncoder needs consistent datatype
event_2 = event_2.fillna(0).astype('str')

# Encode the events
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
event_1['Name'] = labelencoder.fit_transform(event_1['Name'])
event_1['Type'] = labelencoder.fit_transform(event_1['Type'])

event_2['Name'] = labelencoder.fit_transform(event_2['Name'])
event_2['Type'] = labelencoder.fit_transform(event_2['Type'])


# CA_1 + FOODS data only
# Transpose date & Quantity:
Foods = csv_TrainValidation['cat_id'] == 'FOODS'
Cali = csv_TrainValidation['store_id'] == 'CA_1'
TrainValidation_Foods_CA = csv_TrainValidation[Foods][Cali]
# pd.melt(TrainValidation_Foods, value_vars = ['d_1', 'd_2', 'd_3', 'd_4', 'd_5'])
CA_Foods_Transpose = pd.melt(TrainValidation_Foods_CA, id_vars = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'])


# Merge with calendar data with event encoding
csv_calendar['event_name_1_encoding'] = event_1['Name']
csv_calendar['event_type_1_encoding'] = event_1['Type']
csv_calendar['event_name_2_encoding'] = event_2['Name']
csv_calendar['event_type_2_encoding'] = event_2['Type']

new_df = pd.merge(CA_Foods_Transpose, csv_calendar, left_on = 'variable', right_on = 'd')


# Merge with SellPrices data with store_id + item_id
new_df['StoreID + ItemID'] = new_df['store_id'].astype('str') + new_df['item_id'].astype('str')
csv_SellPrices['StoreID + ItemID_SP'] = csv_SellPrices['store_id'].astype('str') + csv_SellPrices['item_id'].astype('str')

df_Sell_Quantity = new_df[['StoreID + ItemID', 'variable', 'value']]
df_Sell_Prices = csv_SellPrices[['StoreID + ItemID_SP', 'sell_price']]
df_Sell_Prices = df_Sell_Prices.loc[368000:700000]
# df_Sell_Prices = df_Sell_Prices.filter(like = 'FOODS', axis = 0)

new_df_with_price = df_Sell_Quantity.merge(df_Sell_Prices, left_on = 'StoreID + ItemID', right_on = 'StoreID + ItemID_SP')



# Split the dataset into Training set & Test set
new_df['sell_quantity'] = new_df['value']
X = new_df['sell_quantity']
y = new_df_with_price['sell_price']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/4, random_state = 0)



