import datetime

import os

import chardet
import loguru
import pyquery
import requests

from optionsClass import OptionsDailyInfo


def main(year, month, day):
    data = {
    "queryType": 2,
    "marketCode": 0,
    "dateaddcnt": "",
    "commodity_id": "MTX",
    "commodity_id2": "",
    "queryDate": f'{year}/{month:02}/{day:02}',
    "MarketCode": 0,
    "commodity_idt": "MTX",
    "commodity_id2t": "",
    "commodity_id2t2": ""
    }
    resp = requests.post('https://www.taifex.com.tw/cht/3/futDailyMarketReport', data = data)
    
    if resp.status_code != 200:
        loguru.logger.error('RESP: status code is not 200')
    loguru.logger.success('RESP: success')

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

    if txt is None:
        return
    # loguru.logger.info(txt)

    # proportions = []

    d = pyquery.PyQuery(txt)
    
    trs = list(d('div#printhere table').items())[2]
    trs = list(trs('tr').items())[1:]
    

    contractMonthWeek = ""
    contractMonthWeekList = []

    optionsDailyInfosPut = []
    optionsDailyInfosCall = []

    for tr in trs:
        tds = list(tr('td').items())

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

            # loguru.logger.info(ContractMonthWeek)

            if contractMonthWeek != ContractMonthWeek:
                # loguru.logger.info("Different")
                contractMonthWeek = ContractMonthWeek
                contractMonthWeekList.append(ContractMonthWeek)
                optionsDailyInfosPut.append([])
                optionsDailyInfosCall.append([])
            
            if CallPut == "Put":
                optionsDailyInfosPut[-1].append(OptionsDailyInfo(
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
                ))
            if CallPut == "Call":
                optionsDailyInfosCall[-1].append(OptionsDailyInfo(
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
                ))
    loguru.logger.info(contractMonthWeek)
    
    m = []
    # for optionsDailyInfo in optionsDailyInfosPut:
    #     for optionsDailyInfoMonthWeek in optionsDailyInfo:
    #         m.append(str(optionsDailyInfoMonthWeek))

    for optionsDailyInfo in optionsDailyInfosCall:
        for optionsDailyInfoMonthWeek in sorted(optionsDailyInfo, key=lambda s: s.VolumeTotal):
            m.append(str(optionsDailyInfoMonthWeek))
        # break
    
    message = os.linesep.join(m)
    

    # 將每筆物件表達式輸出的字串以系統換行符號相接，讓每筆物件表達式各自獨立一行
    
    loguru.logger.info('OptionsDailyInfo' + os.linesep + message)

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    main(2020, 5, 21)