import csv
import datetime
import os
import random

import loguru

from getProxy import getProxiesFromProxyNova, getProxiesFromGatherProxy, getProxiesFromFreeProxyList

import requests
import requests.exceptions

now = datetime.datetime.now()
proxies = []

# 隨機取出一組代理
def getProxy():
    global proxies
    # 若代理清單內已無代理，則重新下載
    if len(proxies) == 0:
        getProxies()
    proxy = random.choice(proxies)
    loguru.logger.debug(f'getProxy: {proxy}')
    proxies.remove(proxy)
    loguru.logger.debug(f'getProxy: {len(proxies)} proxies is unused.')
    return proxy

def reqProxies(hour):
    global proxies
    proxies = proxies + getProxiesFromProxyNova()
    proxies = proxies + getProxiesFromGatherProxy()
    proxies = proxies + getProxiesFromFreeProxyList()
    proxies = list(dict.fromkeys(proxies))
    loguru.logger.debug(f'reqProxies: {len(proxies)} proxies is found.')

def getProxies():
    global proxies
    hour = f'{now:%Y%m%d%H}'
    filename = f'proxies-{hour}.csv'
    filepath = f'{filename}'
    if os.path.isfile(filepath):
        loguru.logger.info(f'getProxies: {filename} exists.')
        loguru.logger.warning(f'getProxies: {filename} is loading...')
        with open(filepath, 'r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                proxy = row['Proxy']
                proxies.append(proxy)
        loguru.logger.success(f'getProxies: {filename} is loaded.')
    else:
        loguru.logger.info(f'getProxies: {filename} does not exist.')
        reqProxies(hour)
        loguru.logger.warning(f'getProxies: {filename} is saving...')
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Proxy'
            ])
            for proxy in proxies:
                writer.writerow([
                    proxy
                ])
        loguru.logger.success(f'getProxies: {filename} is saved.')

# 用於保存上一次連線請求成功時用的代理資訊
proxy = None

def testRequest():
    global proxy
    # 持續更換代理直到連線請求成功為止
    while True:
        # 若無上一次連線請求成功的代理資訊，則重新取出一組代理資訊
        if proxy is None:
            proxy = getProxy()
        try:
            url = f'https://www.google.com/'
            loguru.logger.info(f'testRequest: url is {url}')
            loguru.logger.warning(f'testRequest: downloading...')
            response = requests.get(
                url,
                # 指定 HTTPS 代理資訊
                proxies={
                    'https': f'https://{proxy}'
                },
                # 指定連限逾時限制
                timeout=5
            )
            if response.status_code != 200:
                loguru.logger.debug(f'testRequest: status code is not 200.')
                # 請求發生錯誤，清除代理資訊，繼續下個迴圈
                proxy = None
                continue
            loguru.logger.success(f'testRequest: downloaded.')
        # 發生以下各種例外時，清除代理資訊，繼續下個迴圈
        except requests.exceptions.ConnectionError:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working (connection error).')
            proxy = None
            continue
        except requests.exceptions.ConnectTimeout:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working (connect timeout).')
            proxy = None
            continue
        except requests.exceptions.ProxyError:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working (proxy error).')
            proxy = None
            continue
        except requests.exceptions.SSLError:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working (ssl error).')
            proxy = None
            continue
        except Exception as e:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working.')
            loguru.logger.error(e)
            proxy = None
            continue
        # 成功完成請求，離開迴圈
        break
testRequest()