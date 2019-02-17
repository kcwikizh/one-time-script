#!/usr/bin/env python3

import os
import sys
import string
import asyncio
import aiohttp

DOWNLOAD = True
TIMEOUT = 60 # requests timeout /s
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

async def downloadFile(resp, filename):
    chunkSize = 512 * 1024
    with open(filename, 'wb') as f:
        while True:
            chunk = await resp.content.read(chunkSize)
            if not chunk:
                break
            f.write(chunk)
    return

async def fetch(url, session):
    try:
        async with session.get(url, timeout=TIMEOUT) as resp:
            status = resp.status
            # print(url, status)
            if status == 200:
                if DOWNLOAD:
                    filename = url.split('/')[-1]
                    print('downloading', filename)
                    await downloadFile(resp, filename)
                    print('download completed', filename)
    except:
        print(url, 'fail')

def search_link(bgmId) -> None:
    conn = aiohttp.TCPConnector(limit=LIMIT)
    session = aiohttp.ClientSession(connector=conn)
    loop = asyncio.get_event_loop()
    coros = [asyncio.ensure_future(fetch(TEMPLATE_URL.format(bgmId=bgmId, char=c), session)) for c in string.ascii_lowercase[:26]]
    loop.run_until_complete(asyncio.wait(coros))
    loop.run_until_complete(session.close())
    print('finish')

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['h', 'help', '-h', '--help']:
        printHelp()
        return

    bgmId = sys.argv[1]
    if not is_number(bgmId):
        print('参数 bgmId 必须为数字')
        printHelp()
        return
    search_link(bgmId)

if __name__ == '__main__':
    main()
