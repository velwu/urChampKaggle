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


# FOODS data only
# Transpose date & Quantity:
Foods = csv_TrainValidation['cat_id'] == 'FOODS'
TrainValidation_Foods = csv_TrainValidation[Foods]
# pd.melt(TrainValidation_Foods, value_vars = ['d_1', 'd_2', 'd_3', 'd_4', 'd_5'])
Foods_Transpose = pd.melt(TrainValidation_Foods, id_vars = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'])


# merge with calendar data with event encoding
csv_calendar['event_name_1_encoding'] = event_1['Name']
csv_calendar['event_type_1_encoding'] = event_1['Type']
csv_calendar['event_name_2_encoding'] = event_2['Name']
csv_calendar['event_type_2_encoding'] = event_2['Type']

new = pd.merge(Foods_Transpose, csv_calendar, left_on = 'variable', right_on = 'd')
