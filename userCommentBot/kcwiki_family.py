# -*- coding: utf-8  -*-
'''
amilies/kcwiki_family.py

KCWiki family

https://www.mediawiki.org/wiki/Manual:Pywikibot/Use_on_third-party_wikis
'''
from pywikibot import family

# The official kcwiki Wiki. #Put a short project description here.

class Family(family.Family):

    def __init__(self):
        family.Family.__init__(self)
        self.name = 'kcwiki' # Set the family name; this should be the same as in the filename.
        self.langs = {
            'zh': 'zh.kcwiki.org', # Put the hostname here.
       }

    def protocol(self, code):
        return 'HTTPS'

    def version(self, code):
        # TODO update correct version
        return "1.4.2"  # The MediaWiki version used. Not very important in most cases.

    def scriptpath(self, code):
        return '' # The relative path of index.php, api.php : look at your wiki address.
# This line may need to be changed to /wiki or /w,
# depending on the folder where your mediawiki program is located.
# Note: Do not _include_ index.php, etc.
