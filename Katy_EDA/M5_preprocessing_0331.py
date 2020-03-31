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
