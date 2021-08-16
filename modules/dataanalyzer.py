import json
import math
import time
from modules.getTags import gettagsbycharacter
import asyncio
# data = {
#     'theresa (arknights)': {
#         'count': 1,
#         'tags': ['2girls', 'ass', 'breasts', 'cleft of venus', 'ddddecade', 'multiple girls', 'nude', 'pussy', 'red eyes', 'sex', 'white hair', 'yuri', 'cameltoe']},
#     'w (arknights)': {
#         'count': 1,
#         'tags': ['2girls', 'ass', 'breasts', 'cleft of venus', 'ddddecade', 'multiple girls', 'nude', 'pussy', 'red eyes', 'sex', 'white hair', 'yuri', 'cameltoe']}}

def timber(data):
    _data = {}
    for char in data:
        _data[char] = {}
        _data[char]['total'] = 0
        _data[char]['count'] = data[char]['count']
        _data[char]['tags'] = {}
        for tags in data[char]['tags']:
            if tags not in _data[char]['tags']:
                _data[char]['tags'][tags] = 0
            _data[char]['tags'][tags] += 1
            _data[char]['total'] +=1
    return _data

def databuilder(keywords,src=None):
    __data =  gettagsbycharacter(keywords,src)
    # __data = gettagsbycharacter(keywords)
    # with open('./catch/gettags_1628777267.json') as a:
    #     __data = json.load(a)
    data = timber(__data)
    _data = {}
    for char in data:
        _data[char] = {}
        for tags in data[char]['tags']:
            _tag = data[char]['tags'][tags]
            ___1 = data[char]['count']
            _data[char][tags] = [_tag,round(_tag/data[char]['count']*100,3),round(_tag/data[char]['total']*100,3)]  #[数量，占作品比，占总tag数量比]
    _name = './catch/dataanalyze_' + keywords.replace(':','_') + '#' + str(math.floor(time.time())) + '.json'
    with open(_name,'w',encoding='utf-8') as F:
        F.write(json.dumps(_data))
        return _data

