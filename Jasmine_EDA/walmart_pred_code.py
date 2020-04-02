# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:05:51 2020

@author: Jasmine Kuo
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

calendar = pd.read_csv(r'G:\我的雲端硬碟\UIUC-IS\Kaggle\m5-forecasting-accuracy\calendar.csv')
sales = pd.read_csv(r'G:\我的雲端硬碟\UIUC-IS\Kaggle\m5-forecasting-accuracy\sales_train_validation.csv')
sell_price = pd.read_csv(r'G:\我的雲端硬碟\UIUC-IS\Kaggle\m5-forecasting-accuracy\sell_prices.csv')

for_use = sales.iloc[:,:-28]
valid = pd.concat([sales.iloc[:,:6], sales.iloc[:,-28:]], axis = 1)

# Group by category & state
for_use[(for_use['cat_id']=='HOBBIES')&(for_use['state_id']=='CA')].shape
sales_g1 = for_use[(for_use['cat_id']=='HOBBIES')&(for_use['state_id']=='CA')]

# Transform the data
sales_g1_melt = pd.melt(sales_g1, id_vars=sales_g1.columns[:6], value_vars=sales_g1.columns[6:])
sales_g1_melt.columns = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id', 'd', 'sales']

# Merge all dataset
sales_g1_melt_merge = pd.merge(sales_g1_melt, calendar)
sales_g1_melt_merge = pd.merge(sales_g1_melt_merge, sell_price, how = 'left')
sales_g1_melt_merge = sales_g1_melt_merge.sort_values(['id', 'date']).reset_index(drop = True)

# Drop some useless columns
df = sales_g1_melt_merge[['item_id', 'dept_id', 'store_id', 'd', 'sales', 'wm_yr_wk', 'wday', 'month', 'year',
                          'event_name_1', 'event_name_2', 'snap_CA', 'snap_TX', 'snap_WI', 'sell_price']].copy()

df['event_name_1'] = (df['event_name_1'].notnull()).astype('int')
df['event_name_2'] = (df['event_name_2'].notnull()).astype('int')
df['wm_yr_wk'] = df['wm_yr_wk'].apply(lambda x: int(str(x)[-2:]))

train = df.loc[df['d'].isin(list(df['d'].unique()[:-28]))]
test = df.loc[df['d'].isin(list(df['d'].unique()[-28:]))]

#test['sell_price'].isna().sum()

train = train[train['sell_price'].notna()]
X_train = train[['wm_yr_wk', 'wday', 'month', 'year', 'event_name_1', 'event_name_2', 'snap_CA', 'snap_TX', 'snap_WI', 'sell_price']]
y_train = train['sales']
X_test = test[['wm_yr_wk', 'wday', 'month', 'year', 'event_name_1', 'event_name_2', 'snap_CA', 'snap_TX', 'snap_WI', 'sell_price']]
y_test = test['sales']

import xgboost as xgb
xg_reg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 5, alpha = 10, n_estimators = 10)
xg_reg.fit(X_train,y_train)
preds = xg_reg.predict(X_test)




