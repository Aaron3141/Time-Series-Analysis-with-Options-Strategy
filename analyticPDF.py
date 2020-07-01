import ctypes
import datetime
import os

import camelot
import camelot.ext.ghostscript._gsprint
import loguru
import requests

camelot.ext.ghostscript._gsprint.c_stdstream_call_t = ctypes.CFUNCTYPE(
    ctypes.c_int,
    camelot.ext.ghostscript._gsprint.gs_main_instance,
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_int
)

def main(code):
    resp = requests.get(f'https://www.twse.com.tw/pdf/ch/{code}_ch.pdf')
    if resp.status_code != 200:
        loguru.logger.error('RESP: status code is not 200')
    loguru.logger.success('RESP: success')

    filename = f'{code}.pdf'
    filepath = f'{filename}'

    with open(filepath, 'wb') as f:
        f.write(resp.content)

    # 透過 camelot 辨識出 PDF 檔案內的表格
    tables = camelot.read_pdf(filepath)
    loguru.logger.info('DataFrame' + os.linesep + repr(tables[0].df))

    # 取出第 1 表格的 DataFrame 中的實收資本額
    paidin = tables[0].df[0][3]
    paidin.replace('新台幣', '').replace(',', '').strip()
    loguru.logger.info(f'實收資本額 {paidin}')

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    # 傳入股票代碼
    main('1101')