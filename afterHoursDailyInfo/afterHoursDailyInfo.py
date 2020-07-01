
import csv
import datetime
import os
import io

import loguru
import requests

from afterHoursDailyInfoClass import AfterHoursDailyInfo

def main(year, month, code):
    date = f'{year}{month:02}01'
    resp = requests.get(
        f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?' +
        f'response=csv&date={date}&stockNo={code}')
    if resp.status_code != 200:
        loguru.logger.error('RESP: status code is not 200')
    loguru.logger.success('RESP: success')

    # 個股每月各交易日盤後資訊清單
    afterHoursDailyInfos = []
    # 取出 CSV 內容，並去除第一行及最後 5 行
    lines = io.StringIO(resp.text).readlines()
    lines = lines[1:-5]
    # 透過 CSV 讀取器載入
    reader = csv.DictReader(io.StringIO('\n'.join(lines)))
    # 依序取出每筆資料行
    for row in reader:
        # 取出日期欄位值
        date = row['日期'].strip()
        # 取出成交股數欄位值
        totalShare = row['成交股數'].replace(',', '').strip()
        # 取出成交金額欄位值
        totalTurnover = row['成交金額'].replace(',', '').strip()
        # 取出開盤價欄位值
        openPrice = row['開盤價']
        # 取出最高價欄位值
        highestPrice = row['最高價']
        # 取出最低價欄位值
        lowestPrice = row['最低價']
        # 取出收盤價欄位值
        closePrice = row['收盤價']
        afterHoursDailyInfo = AfterHoursDailyInfo(
            code=code,
            date=date,
            totalShare=totalShare,
            totalTurnover=totalTurnover,
            openPrice=openPrice,
            highestPrice=highestPrice,
            lowestPrice=lowestPrice,
            closePrice=closePrice
        )
        afterHoursDailyInfos.append(afterHoursDailyInfo)
    loguru.logger.info(afterHoursDailyInfos)

    # 將每筆物件表達式輸出的字串以系統換行符號相接，讓每筆物件表達式各自獨立一行
    message = os.linesep.join([
        str(afterHoursDailyInfo)
        for afterHoursDailyInfo in afterHoursDailyInfos
    ])
    loguru.logger.info('AFTERHOURSDAILYINFOS' + os.linesep + message)

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    # 傳入年、月及股票代碼
    main(2020, 4, '1101')