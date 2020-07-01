import datetime
import fractions
import json
import os
import re

import loguru
import requests

from aterHoursInfoClass import AfterHoursInfo

def main():
    resp = requests.get(
        f'https://www.twse.com.tw/exchangeReport/MI_INDEX?' +
        f'response=json&' +
        f'type=ALLBUT0999' +
        # f'&date={datetime.date.today():%Y%m%d}'
        f'&date=20200518'
    )
    if resp.status_code != 200:
        loguru.logger.error('RESP: status code is not 200')
    loguru.logger.success('RESP: success')

    afterHoursInfos = []

    body = resp.json()
    stat = body['stat']
    if stat != 'OK':
        loguru.logger.error(f'RESP: body.stat error is {stat}.')
        return
    records = body['data9']
    for record in records:
        code = record[0].strip()
        if re.match(r'^[1-9][0-9][0-9][0-9]$', code) is not None:
            name = record[1].strip()
            totalShare = record[2].replace(',', '').strip()
            totalTurnover = record[4].replace(',', '').strip()
            openPrice = record[5].replace(',', '').strip()
            highestPrice = record[6].replace(',', '').strip()
            lowestPrice = record[7].replace(',', '').strip()
            closePrice = record[8].replace(',', '').strip()
            afterHoursInfo = AfterHoursInfo(
                code=code,
                name=name,
                totalShare=totalShare,
                totalTurnover=totalTurnover,
                openPrice=openPrice,
                highestPrice=highestPrice,
                lowestPrice=lowestPrice,
                closePrice=closePrice
            )
            afterHoursInfos.append(afterHoursInfo)

    message = os.linesep.join([
        str(afterHoursInfo)
        for afterHoursInfo in afterHoursInfos
    ])
    loguru.logger.info('AFTERHOURSINFOS' + os.linesep + message)

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    main()