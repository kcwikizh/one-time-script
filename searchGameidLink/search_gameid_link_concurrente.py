#!/usr/bin/env python3

import os
import sys
import string
import requests
import concurrent.futures

DOWNLOAD = True
TIMEOUT = 10 # requests timeout /s
LIMIT = 5
TEMPLATE_URL = 'http://cn.kcwiki.org/kcs/resources/bgm_p/{bgmId}{char}.swf'

def printHelp():
    print('''kcwiki家具bgm下载地址查找
自动从 {url} 查找正确的家具bgm下载地址并下载
用法:
    python {file} [bgmId]
使用 "python {file} --help" 查看帮助。
'''.format(file=os.path.basename(__file__), url=TEMPLATE_URL))

def is_number(s) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

def downloadFile(resp, filename):
    chunkSize = 512 * 1024
    with open(filename, 'wb') as f:
        for block in resp.iter_content(chunkSize):
            f.write(block)
    return True

def fetch(url):
    try:
        resp = requests.get(url, timeout=TIMEOUT, stream=True)
        status = resp.status_code
        # print(url, status)
        if status == 200:
            if DOWNLOAD:
                filename = url.split('/')[-1]
                print('downloading', filename)
                downloadFile(resp, filename)
                print('download completed', filename)
            return True
    except:
        print(url, 'fail')
    return False

def search_link(bgmId) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=LIMIT) as executor:
        [executor.submit(fetch, TEMPLATE_URL.format(bgmId=bgmId, char=c)) for c in string.ascii_lowercase[:26]]

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['h', 'help', '-h', '--help']:
        printHelp()
        return

    for i in range(1, len(sys.argv)):
        bgmId = sys.argv[i]
        if not is_number(bgmId):
            print('参数 bgmId 必须为数字')
            printHelp()
            return
        print('searching', bgmId)
        search_link(bgmId)
    print('finish')


if __name__ == '__main__':
    main()
