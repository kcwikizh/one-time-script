#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import os
import time
from kcwikibot import KcWikiBot
import pywikibot

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') #改变标准输出的默认编码

import asyncio
from concurrent.futures import ThreadPoolExecutor

async def getNewestTopic(self, page):
    api = self.apiSite
    topiclist = api.load_topiclist(page)
    # topiclist = api.load_board(page)

    roots = topiclist.get('roots')
    if len(roots) < 1:
        return None
    posts = topiclist.get('posts')
    firstPost = posts.get(roots[0])
    firstTitle = topiclist.get('revisions').get(firstPost[0]).get('properties').get('topic-of-post').get('plaintext')
    # print(topiclist.get('revisions').get(firstPost[0]).get('articleTitle'))
    return firstTitle

def  validation(str):
    pass

async def work():
    USER_LIST = 'user-list.txt'
    FILE_PATH = 'template.txt'
    topicTitle = '感谢您在kcwiki的贡献!'

    with open(FILE_PATH, 'r', encoding='utf_8') as f:
        content = f.read()
    # content = 'If you can read this, the Flow code in Pywikibot works!'

    kcwikibot = KcWikiBot()
    with open(USER_LIST, 'r', encoding='utf_8') as f:
        user = True
        no = 0
        while user:
            user = f.readline().strip()
            no = no + 1
            if len(user) == 0:
                print('{}. 空行 结束'.format(no), flush=True)
                break;
            if user.find('机器人') >= 0:
                # 过滤机器人 * 假设正常用户用户名不含'机器人'
                print('{}. 发现机器人 {}'.format(no, user))
                continue;
            username = user.split('（')[0] # 过滤用户名
            if len(username) < 1:
                print('{}. 用户名为空 {}'.format(no, user))
                continue
            prefix = 'User_talk:'
            page = prefix + username
            try:
                title = await getNewestTopic(kcwikibot, page)
            except Exception as e:
                print('{}. 获取标题失败  跳过更新'.format(no), flush=True)
                continue

            if title and title.find(topicTitle) >= 0:
            # if False:
                print('{}. {} 最新topic标题 跳过更新 {}'.format(no, username, title), flush=True)
                continue
            print('{}. {} 最新topic标题 {}'.format(no, username, title), flush=True)

            # newTopic
            try:
                wikitext = kcwikibot.newTopic(page, topicTitle, content)
            except Exception as e:
                print('失败', flush=True)
                # raise(e)
            else:
                if wikitext:
                    print('成功',flush=True)
            sys.stdout.flush() # 强制立刻刷新缓冲

if __name__ == '__main__':
    print('KcWiki Robot: 开始创建 topic...', flush=True)
    START = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(work())
    loop.close()
    # work()

    END = time.time()
    DELTA = END - START
    print('KcWiki Robot: 任务已完成，共用时：{0}s.'.format(round(DELTA, 3)))
