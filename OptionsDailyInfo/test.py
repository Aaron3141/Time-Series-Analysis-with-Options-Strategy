import datetime

import os

import chardet
import loguru
import pyquery
import requests

from optionsClass import OptionsDailyInfo
data = {
    "queryType": 2,
    "marketCode": 0,
    "dateaddcnt": "",
    "commodity_id": "TXO",
    "commodity_id2": "",
    "queryDate": "2020/05/19",
    "MarketCode": 0,
    "commodity_idt": "TXO",
    "commodity_id2t": "",
    "commodity_id2t2": ""
}
resp = requests.post('https://www.taifex.com.tw/cht/3/optDailyMarketReport', data = data)

txt = None
det = chardet.detect(resp.content)
try:
    if det['confidence'] > 0.5:
        if det['encoding'] == 'big-5':
            txt = resp.content.decode('big5')
        else:
            txt = resp.content.decode(det['encoding'])
    else:
        txt = resp.content.decode('utf-8')
except Exception as e:
    loguru.logger.error(e)
# print(txt)

d = pyquery.PyQuery(txt)
# asd = list(d('div#printhere table tr').items())
# print(asd)
trs = list(d('div#printhere table').items())[2]
# print(trs[2])
# trs = trs[1:]
trs = list(trs('tr').items())[1:]
# print(tds)
# code = trs[0]
# print("code", code)
for tr in trs:
    tds = list(tr('td').items())
    # for td in tds:
    #     print(td.text().strip(), end="    ")
    # print()
    # print(tds[0].text().strip())
    if tds[0].text().strip() == "TXO":
        ContractMonthWeek=tds[1].text().strip()
        StrikePrice=tds[2].text().strip()
        CallPut=tds[3].text().strip()
        Open=tds[4].text().strip()
        High=tds[5].text().strip()
        Low=tds[6].text().strip()
        Close=tds[7].text().strip()
        Change=tds[9].text().strip()
        Percent=tds[10].text().strip()
        VolumeAfterHours=tds[11].text().strip()
        VolumeRegular=tds[12].text().strip()
        VolumeTotal=tds[13].text().strip()
        OpenInterest=tds[14].text().strip()
        BestBid=tds[15].text().strip()
        BestAsk=tds[16].text().strip()
        HistoricalHigh=tds[17].text().strip()
        HistoricalLow=tds[18].text().strip()
        
        t = OptionsDailyInfo(
        ContractMonthWeek,
        StrikePrice,
        CallPut,
        Open,
        High,
        Low,
        Close,
        Change,
        Percent,
        VolumeAfterHours,
        VolumeRegular,
        VolumeTotal,
        OpenInterest,
        BestBid,
        BestAsk,
        HistoricalHigh,
        HistoricalLow
        )
    
        print(t)
        print()
