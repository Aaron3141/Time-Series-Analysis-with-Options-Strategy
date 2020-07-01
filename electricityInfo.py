import csv
import datetime
import io
import pandas
import plotly.graph_objects
import os

import loguru
import requests



def main():
    mm = int(f'{datetime.date.today():%m}')-1
    filepath = f'electricityInfo-{datetime.date.today():%Y}{mm:02}.csv'
    filename = f'{filepath}'

    if not os.path.isfile(filepath):
        loguru.logger.info(f'electricityInfo: {filename} does not exist.')
        resp = requests.get(
        f'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/sys_dem_sup.csv')
        if resp.status_code != 200:
            loguru.logger.error('RESP: status code is not 200')
        loguru.logger.success('RESP: success')

        # 個股每月各交易日盤後資訊清單
        afterHoursDailyInfos = []
        # 取出 CSV 內容
        lines = io.StringIO(resp.text).readlines()
        
        # 透過 CSV 讀取器載入
        reader = csv.reader(io.StringIO(''.join(lines)))

        loguru.logger.warning(f'electricityInfo: {filename} is saving...')

        with open(filepath, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date',
                'Industrial',
                'GeneralPublic'
            ])
            for row in reader:
                writer.writerow([
                    row[0],
                    row[5],
                    row[6]
                ])
        loguru.logger.success(f'electricityInfo: {filename} is saved.')
        
    else:
        loguru.logger.info(f'electricityInfo: {filename} exists.')
        
    loguru.logger.warning(f'electricityInfo: {filename} is loading...')
    loguru.logger.success(f'electricityInfo: {filename} is loaded.')

    df = pandas.read_csv(filepath)
    dfTa = pandas.read_csv('taiexs-2019.csv')

    df['Date'] = pandas.to_datetime(df['Date'], format='%Y%m%d')
    df.index = df['Date'] 
    dff = df.resample('1W').mean()

    dfTa['Date'] = pandas.to_datetime(dfTa['Date'], format='%Y%m%d')
    dfTa['ClosePrice'] = dfTa['ClosePrice'].apply(lambda x : x / 100)
    dfTa.index = dfTa['Date'] 
    dffTa = dfTa.resample('1W').mean()
    figure = plotly.graph_objects.Figure(
        data=[
            # Line Chart
            # 收盤價
            plotly.graph_objects.Scatter(
                # x=dff['Date'],
                x=dff.index,
                y=dff['Industrial'],
                name='Industrial',
                mode='lines',
                line=plotly.graph_objects.scatter.Line(
                    color='#6B99E5'
                )
            ),
            plotly.graph_objects.Scatter(
                x=dff.index,
                y=dff['GeneralPublic'],
                name='GeneralPublic',
                mode='lines',
                line=plotly.graph_objects.scatter.Line(
                    color='#ff79ff'
                )
            ),
            plotly.graph_objects.Scatter(
                x=dffTa.index,
                y=dffTa['ClosePrice'],
                name='ClosePrice',
                mode='lines',
                line=plotly.graph_objects.scatter.Line(
                    color='#ffe500'
                )
            )
            # Candlestick Chart
            # K 棒
            # plotly.graph_objects.Candlestick(
            #     x=df['Date'],
            #     open=df['OpenPrice'],
            #     high=df['HighestPrice'],
            #     low=df['LowestPrice'],
            #     close=df['ClosePrice'],
            #     name='盤後資訊',
            # )
        ],
        # 設定 XY 顯示格式
        layout=plotly.graph_objects.Layout(
            xaxis=plotly.graph_objects.layout.XAxis(
                tickformat='%Y-%m-%d'
            ),
            yaxis=plotly.graph_objects.layout.YAxis(
                tickformat='.2f'
            )
        )
    )
    figure.show()
    # # 將每筆物件表達式輸出的字串以系統換行符號相接，讓每筆物件表達式各自獨立一行
    # message = os.linesep.join([
    #     str(afterHoursDailyInfo)
    #     for afterHoursDailyInfo in afterHoursDailyInfos
    # ])
    loguru.logger.info('Figure Show')

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    # 傳入年、月及股票代碼
    main()