import datetime

import os

import chardet
import loguru
import pyquery
import requests
import io
import csv
import pandas

import sys
sys.path.insert(1, '//Users/singularity/Aaron/coding/fintech')

from getProxy import getProxy

proxy, proxies = getProxy([])



# from optionsClass import OptionsDailyInfo
def getOptions(year, month, day):
    global proxies, proxy
    while True:
        if proxy is None:
            proxy, proxies = getProxy(proxies)
        filename = f'optionsDailyInfo-{year}{month:02}{day:02}.csv'
        filepath = f'/Users/singularity/Aaron/coding/fintech/OptionsDailyInfoData/{filename}'
        loguru.logger.info(filename)
        data = {
            "down_type": "1",
            "commodity_id": "TXO",
            "commodity_id2": "",
            "queryStartDate": f'{year}/{month:02}/{day:02}',
            "queryEndDate": f'{year}/{month:02}/{day:02}'
        }
        url = 'https://www.taifex.com.tw/cht/3/optDataDown'
        loguru.logger.warning(f'optionsDailyInfo: {year}{month:02}{day:02} is downloading...')
        try:
            response = requests.post(
                url,
                proxies={
                    'https': f'https://{proxy}'
                },
                data = data,
                timeout=3
            )
            if response.status_code != 200:
                loguru.logger.success(f'optionsDailyInfo: {year}{month:02}{day:02} responses with error({response.status_code}).')
                proxy = None
                break
            loguru.logger.success(f'optionsDailyInfo: month {month} is downloaded.')
            # 取出 CSV 內容
            lines = io.StringIO(response.text).readlines()
            # print(lines[0:5])
            if len(lines) == 1:
                loguru.logger.error(f'optionsDailyInfo: {filename} data not exists.')
                break
            # 透過 CSV 讀取器載入
            reader = csv.DictReader(io.StringIO(''.join(lines)))
            # print(reader)
            # 依序取出每筆資料行
            loguru.logger.info(f'optionsDailyInfo: {filename} is saving.')
            with open(filepath, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ContractMonthWeek",
                    "StrikePrice",
                    "CallPut",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "OpenInterest",
                    "BestBid",
                    "BestAsk",
                    "HistoricalHigh",
                    "HistoricalLow",
                    "Session"
                ])
                for row in reader:
                    writer.writerow([
                        row["到期月份(週別)"],
                        row["履約價"],
                        "Call" if row["買賣權"] == "買權" else "Put",
                        row["開盤價"],
                        row["最高價"],
                        row["最低價"],
                        row["收盤價"],
                        row["成交量"],
                        row["未沖銷契約數"],
                        row["最後最佳買價"],
                        row["最後最佳賣價"],
                        row["歷史最高價"],
                        row["歷史最低價"],
                        "Regular" if row["交易時段"] == "一般" else "AfterHours"
                    ])
            loguru.logger.success(f'optionsDailyInfo: {filename} is saved.')
            # body = response.json()
            # stat = body['stat']
            # if stat != 'OK':
            #     loguru.logger.error(f'optionsDailyInfo: month {month} responses with error({stat}).')
            #     break
            # records = body['data']
            # if len(records) == 0:
            #     loguru.logger.success(f'optionsDailyInfo: month {month} has no data.')
            #     break
            # for record in records:
            #     date = record[0].strip()
            #     parts = date.split('/')
            #     y = int(parts[0]) + 1911
            #     m = int(parts[1])
            #     d = int(parts[2])
            #     date = f'{y}{m:02d}{d:02d}'
            #     openPrice = record[1].replace(',', '').strip()
            #     highestPrice = record[2].replace(',', '').strip()
            #     lowestPrice = record[3].replace(',', '').strip()
            #     closePrice = record[4].replace(',', '').strip()
            #     taiex = Taiex(
            #         date=date,
            #         openPrice=openPrice,
            #         highestPrice=highestPrice,
            #         lowestPrice=lowestPrice,
            #         closePrice=closePrice
            #     )
            #     taiexs.append(taiex)
        except requests.exceptions.ConnectionError:
            loguru.logger.error(f'optionsDailyInfo: proxy({proxy}) is not working (connection error).')
            proxy = None
            continue
        except requests.exceptions.ConnectTimeout:
            loguru.logger.error(f'optionsDailyInfo: proxy({proxy}) is not working (connect timeout).')
            proxy = None
            continue
        except requests.exceptions.ProxyError:
            loguru.logger.error(f'optionsDailyInfo: proxy({proxy}) is not working (proxy error).')
            proxy = None
            continue
        except requests.exceptions.SSLError:
            loguru.logger.error(f'optionsDailyInfo: proxy({proxy}) is not working (ssl error).')
            proxy = None
            continue
        except Exception as e:
            loguru.logger.error(f'optionsDailyInfo: proxy({proxy}) is not working.')
            loguru.logger.error(e)
            proxy = None
            continue
        break
    return


def main(year, month, day):
    filename = f'optionsDailyInfo-{year}{month:02}{day:02}.csv'
    filepath = f'/Users/singularity/Aaron/coding/fintech/OptionsDailyInfoData/{filename}'
    loguru.logger.info(filename)
    data = {
        "down_type": "1",
        "commodity_id": "TXO",
        "commodity_id2": "",
        "queryStartDate": f'{year}/{month:02}/{day:02}',
        "queryEndDate": f'{year}/{month:02}/{day:02}'
    }
    
    resp = requests.post('https://www.taifex.com.tw/cht/3/optDataDown', data = data)
    # resp = requests.post('https://www.taifex.com.tw/enl/eng3/optDataDown', data = data)
    if resp.status_code != 200:
        loguru.logger.error('RESP: status code is not 200')
    loguru.logger.success('RESP: success')
    # 取出 CSV 內容
    lines = io.StringIO(resp.text).readlines()
    print(lines[0:5])
    if len(lines) == 1:
        loguru.logger.error(f'optionsDailyInfo: {filename} data not exists.')
        return
    # lines = lines[1:]
    # 透過 CSV 讀取器載入
    reader = csv.DictReader(io.StringIO(''.join(lines)))
    # print(reader)
    # 依序取出每筆資料行
    # if 
    loguru.logger.info(f'optionsDailyInfo: {filename} is saving.')
    with open(filepath, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([
            "ContractMonthWeek",
            "StrikePrice",
            "CallPut",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "OpenInterest",
            "BestBid",
            "BestAsk",
            "HistoricalHigh",
            "HistoricalLow",
            "Session"
        ])
        for row in reader:
            writer.writerow([
                row["到期月份(週別)"],
                row["履約價"],
                "Call" if row["買賣權"] == "買權" else "Put",
                row["開盤價"],
                row["最高價"],
                row["最低價"],
                row["收盤價"],
                row["成交量"],
                row["未沖銷契約數"],
                row["最後最佳買價"],
                row["最後最佳賣價"],
                row["歷史最高價"],
                row["歷史最低價"],
                "Regular" if row["交易時段"] == "一般" else "AfterHours"
            ])
    loguru.logger.success(f'optionsDailyInfo: {filename} is saved.')
    

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    # main(2020,6,21)
    getOptions(2018, 10, 9)
    getOptions(2019, 12, 31)
    # dayRange = pandas.bdate_range(start='6/1/2018', end='6/25/2020', freq="W-MON")
    # for day in dayRange:
    #     getOptions(day.year, day.month, day.day)