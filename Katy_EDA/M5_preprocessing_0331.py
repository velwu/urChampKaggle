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


# FOODS data only:
Foods = csv_TrainValidation['cat_id'] == 'FOODS'
TrainValidation_Foods = csv_TrainValidation[Foods]

# Below part needs modification QQ
to_repeat = TrainValidation_Foods.iloc[:, 1:5]
days_in_one_column = pd.concat([to_repeat] * 1913)
days_in_one_column['day_n'] = pd.concat([pd.Series(range(1, 1914))] * 3)

days_in_one_column['day'] = TrainValidation_Foods['d_1']
'''
for i in range(2, 1914):
    days_in_one_column['day'].append(TrainValidation_Foods[str('d_' + 'i')])   
'''     
days_in_one_column['day'].append(TrainValidation_Foods['d_2'])
days_in_one_column['day'].append(TrainValidation_Foods['d_3'])
