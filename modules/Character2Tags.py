from modules.dataanalyzer import databuilder
import json
import re
# import math
# import time
import asyncio

class Character2Tags:
    def __init__(self):
        pass
    def fromkeyword(self,keyword:str,src = None):
        self.keywords = keyword,
        self.data = databuilder(keyword,src)


    def fromfile(self,src:str):
        with open(src,'r',encoding='utf-8') as f:
            self.data = json.load(f)
        self.keywords = re.search('(?<=dataanalyze_)\w+',src).group(0)
        return True

    def t_tags_d_character(self, tagName:str,copyright:str):
        _result = {}
        _result[tagName] = []
        for char in self.data:
            if tagName in self.data[char]:
                if copyright in char:
                    _result[tagName].append([char.replace('('+ copyright +')',''),self.data[char][tagName][0],self.data[char][tagName][1],self.data[char][tagName][2]])
        return _result
