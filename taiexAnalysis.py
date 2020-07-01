# %%
import csv
import datetime
import io
import pandas
import plotly.graph_objects
# from pandas.tseries.offsets import *

import loguru
import requests

# %%

# mm = int(f'{datetime.date.today():%m}')-1
# filepath = f'electricityInfo-{datetime.date.today():%Y}{mm:02}.csv'
filepath = f'taiexs-2019.csv'
filename = f'{filepath}'

df = pandas.read_csv(filepath)
df['Date'] = pandas.to_datetime(df['Date'], format='%Y%m%d')
df.index = df['Date'] 
# df = df.index >
# df.resample('1W').mean()
df['day_of_week'] = df['Date'].dt.day_name()
# df = df[df['day_of_week']== 'Wednesday']
# df['WEEK ENDING'] = (df['Date'] + pandas.tseries.offsets.Week(weekday=2)).apply(lambda x: x.weekday())
df['WEEK ENDING'] = df['Date'].where( df['Date'] == (( df['Date'] + pandas.tseries.offsets.Week(weekday=2) ) - pandas.tseries.offsets.Week()), df['Date'] + pandas.tseries.offsets.Week(weekday=2))
df
# %%