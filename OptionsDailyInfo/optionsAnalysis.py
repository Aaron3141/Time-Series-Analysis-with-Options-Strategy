
import plotly.graph_objects
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import pandas
import datetime
# from pandas.tseries.offsets import *


# from plotly.offline import init_notebook_mode, iplot
# init_notebook_mode(connected=True) 
# import plotly.express as px
# import plotly.graph_objects as go

import loguru
import requests

# pandas.set_option('display.max_rows', 500)
# import sys
# sys.path.insert(1, '/Users/singularity/Aaron/coding/fintech/OptionsDailyInfoData')

class options:
    def __init__(
        self,
        strikePrice,
        optionsDF,
        PutCall,
        BuySell
        ):
        self.strikePrice = strikePrice
        self.optionsDF = optionsDF
        self.PutCall = PutCall
        self.BuySell = BuySell
        print(f'{self.BuySell}{self.PutCall}@{self.strikePrice}')
    def optionsProfit(self, x):
        Exchange_Fee = -1
        y = [0 for _ in range(len(x))]
        
        t = -1 if self.BuySell == "buy" else 1
        s = -50*t
        er = False
        if len(self.optionsDF[self.optionsDF["StrikePrice"] == self.strikePrice]) == 0:
            print(f'{self.BuySell}{self.PutCall}@{self.strikePrice} NOT EXISTS!')
            #  if self.PutCall == "call" else self.strikePrice += 50
            er = True
            print(f'Change to {self.BuySell}{self.PutCall}@{self.strikePrice}')
        if self.PutCall == "call":
            # print(f'@@@@optionsDF\n{self.optionsDF}')
            # print(f'@@@@{self.BuySell}{self.PutCall}@{self.strikePrice}')
            # print(f'@@@@price\n{self.optionsDF[self.optionsDF["StrikePrice"] == self.strikePrice]["Close_Call"]}')
            if er: self.strikePrice -= 50
            price = float(self.optionsDF[self.optionsDF["StrikePrice"] == self.strikePrice]["Close_Call"])*t
            for i in range(len(x)):
                if x[i] <= self.strikePrice:
                    y[i] = price
                else:
                    price += s
                    y[i] = price
        else:
            if er: self.strikePrice += 50
            price = float(self.optionsDF[self.optionsDF["StrikePrice"] == self.strikePrice]["Close_Put"])*t
            for i in range(len(x)-1,-1,-1):
                if x[i] >= self.strikePrice:
                    y[i] = price
                else:
                    price += s
                    y[i] = price
        # return y
        return np.add(y, np.array([Exchange_Fee for _ in range(len(x))]))
    def optionsScatter(self, x):
        return go.Scatter(
            x=x,
            y=self.optionsProfit(x),
            name = f"{self.BuySell}{self.PutCall}@{self.strikePrice}",
            visible = "legendonly",
            mode='lines',
            # line=go.scatter.Line(color='#6B99E5')
            opacity=0.4
        )



filenameTaiexs = f'taiexs-2019.csv'
filepathTaiexs = f'/Users/singularity/Aaron/coding/fintech/{filenameTaiexs}'

dfTaiexs = pandas.read_csv(filepathTaiexs)
dfTaiexs['Date'] = pandas.to_datetime(dfTaiexs['Date'], format='%Y%m%d')

fileNameSettlementPrice = f'finalSettlementPrice.csv'
filePathSettlementPrice = f'/Users/singularity/Aaron/coding/fintech/{fileNameSettlementPrice}'

dfSettlementPrice = pandas.read_csv(filePathSettlementPrice)
dfSettlementPrice['Date'] = pandas.to_datetime(dfSettlementPrice['Date'], format='%Y/%m/%d')
dfSettlementPrice.sort_values(by='Date', inplace=True)
# dfSettlementPrice["Date"] = dfSettlementPrice["Date"].apply(lambda d:  d-datetime.timedelta(days=2))
dfSettlementPrice["Date"] = dfSettlementPrice.apply(lambda d:  d["Date"]-datetime.timedelta(days=2), axis=1)
dftt = pandas.merge(dfTaiexs, dfSettlementPrice, left_on=["Date"], right_on=["Date"]\
            , suffixes=('_Call','_Put'))[['Date', 'ClosePrice', 'TX/MTX']]


def WinLoss(dftt):
    TAIEX_VALUE = float(dftt['ClosePrice'])
    TAIEX_VALUE_BOTTOM = int(TAIEX_VALUE - (TAIEX_VALUE % 50))
    TAIEX_VALUE_TOP = TAIEX_VALUE_BOTTOM + 50

    TX = float(dftt['TX/MTX'])
    
    DATE = dftt['Date']
    year = f'{DATE:%Y}'
    month = f'{DATE:%m}'
    day = f'{DATE:%d}'

    print(f'{year}/{month}/{day}') ##

    filename = f'optionsDailyInfo-{year}{month}{day}.csv'
    filepath = f'/Users/singularity/Aaron/coding/fintech/OptionsDailyInfoData/{filename}'
    df = pandas.read_csv(filepath)
    ContractMonthWeek = df['ContractMonthWeek'][0]
    StrikePriceLimite = df["StrikePrice"].apply(lambda d: True if int(d)>=TAIEX_VALUE-150 and int(d) <=TAIEX_VALUE+150 else False)
    dfCall = df[(df["CallPut"]=="Call") & (df["Session"]=="Regular") & (df["ContractMonthWeek"]==ContractMonthWeek) & StrikePriceLimite][['ContractMonthWeek', 'StrikePrice','CallPut', 'Close']]
    dfPut = df[(df["CallPut"]=="Put") & (df["Session"]=="Regular") & (df["ContractMonthWeek"]==ContractMonthWeek) & StrikePriceLimite][['ContractMonthWeek', 'StrikePrice','CallPut', 'Close']]
    optionsDF = pandas.merge(dfCall, dfPut, left_on=["StrikePrice", 'ContractMonthWeek'], right_on=["StrikePrice",      'ContractMonthWeek']\
            , suffixes=('_Call','_Put'))[['Close_Call', 'CallPut_Call', 'StrikePrice', 'CallPut_Put', 'Close_Put']]
    # optionsDF.astype({
    #     "Close_Call": "float64",
    #     "CallPut_Call": "string",
    #     "StrikePrice": "int64",
    #     "CallPut_Put": "string",
    #     "Close_Put": "float64"}, errors='ignore')
    x = np.arange(TAIEX_VALUE_BOTTOM-100, TAIEX_VALUE_TOP+200, 50)
    y = [0 for _ in range(len(x))]

    totalOtions = []
    totalOtions.append(options(TAIEX_VALUE_BOTTOM-50, optionsDF, "call", "buy"))
    totalOtions.append(options(TAIEX_VALUE_BOTTOM, optionsDF, "call", "sell"))
    totalOtions.append(options(TAIEX_VALUE_TOP, optionsDF, "put", "sell"))
    totalOtions.append(options(TAIEX_VALUE_TOP+50, optionsDF, "put", "buy"))
    
    y = np.sum([op.optionsProfit(x) for op in totalOtions], axis=0)

    i = 0
    while i <= len(y):
        if TX < x[i]:
            break
        i += 1
    j = i - 1
    if y[i]-y[j] == 0:
        return y[j]
    elif y[i]-y[j] > 0:
        return y[j]+(TX-x[j])
    else:
        return y[j]-(TX-x[j])

dftt["WinLoss"] = dftt.apply(WinLoss, axis=1)
# print(dftt.iloc[9])
# print(WinLoss(dftt.iloc[9]))
print(dftt["WinLoss"].describe())
fig = go.Figure()

fig.add_trace(
    go.Scatter(
            x=dftt["Date"],
            y=dftt["WinLoss"],
            name = f"WinLoss",
            mode='lines'
        ))

fig.update_layout(
    title=f"Profit Graph Taiexs@{TAIEX_VALUE}",
    xaxis_title="x Axis Title",
    yaxis_title="y Axis Title",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="#7f7f7f"
    ),
    xaxis=plotly.graph_objects.layout.XAxis(
        tickformat='%Y-%m-%d'
    ),
    yaxis=plotly.graph_objects.layout.YAxis(
        tickformat='.2f'
    )
)
fig.show()