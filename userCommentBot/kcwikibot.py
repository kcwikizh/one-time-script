#!/usr/bin/python3

import os
import time
import pywikibot
import pywikibot.flow

class KcWikiBot(object):
    """KcWikiBot"""
    def __init__(self, lang='zh', family_name='kcwiki'):
        super(KcWikiBot, self).__init__()
        # 注册 kcwiki family
        file_path = './kcwiki_family.py'
        # pywikibot.config2.register_family_file(family_name, file_path) # !! 会覆盖用户名设置
        # usernames = pywikibot.config2.usernames
        pywikibot.config2.family_files[family_name] = file_path
        # 设定域
        self.site = pywikibot.Site(lang, family_name)
        self.apiSite = pywikibot.site.APISite(lang, family_name)

    def getKcWikiSite(self):
        return self.site

    def updateText(self, page, text, comments='KcWiki Robot: Update {}'
        .format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))):
        """
        更新 wiki 页面
        :param page: 页面
        :param text: 更新后文本
        :param comments: 更新备注
        """
        page = pywikibot.Page(self.site, page)
        # page.text = page.text.replace('foo', 'bar')
        page.text = text
        page.save(comments)  # Saves the page
        return True

    def updateFromFile(self, page, file_path, comments='KcWiki Robot: Update'):
        """
        使用文件更新 wiki 页面
        :param page: 页面
        :param file_path: 文件名
        :param comments: 更新备注
        """
        with open(file_path, 'r', encoding='utf_8') as f:
            text = f.read()
        self.updateText(page, text, comments)
        return True

    def newTopic(self, page, title, content):
        """
        发布新的 topic
        :param page: 页面
        :param file_path: topic 标题
        :param content: topic 内容
        :return 发布文本
        """
        board = pywikibot.flow.Board(self.site, page);
        topic = board.new_topic(title, content, 'wikitext')
        first_post = topic.replies()[0]
        wikitext = first_post.get(format='wikitext')
        return wikitext
