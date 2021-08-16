# from getLinks import getlinks
from modules.getLinks import getlinks
from os import times
import requests
from lxml import html
import math
import json
import time
from modules.headers import headers
import asyncio
import aiohttp

heads = headers()
_links = []
sem = asyncio.Semaphore(10)

def print33(indexnow, indextotal, title):  # 进度条
    A_count = math.floor(indexnow/indextotal*33)
    A = '#'*A_count
    B = '-'*(33-A_count)
    C = math.floor(indexnow/indextotal*1000)/10
    print('>> 正在抓取 |' + A + B + '| ' + str(C) + '% | ' + title, flush=True)


def ifempty(arr):
    if arr[0:1]:
        return arr
    else:
        return ['']


def getnotexist(lstnew, lstold):
    lst = []
    for i in lstnew:
        if i not in lstold:
            lst.append(i)
    return lst

async def req(link,heads,callback=None):
    async with sem:
        async with aiohttp.ClientSession(headers=heads) as client:
            async with client.request('GET',link) as resp:
                _element = await resp.text()
                _links.append(_element)

def fromfile(src):
    data = ''
    with open(src,'r',encoding='utf-8') as F:
        data = json.load(F)
    return data

def gettagsbycharacter(keywords, src = None):
    if src:
        __links = fromfile(src)
    else:
        __links = getlinks(keywords)
    links = __links['links']
    tags = {}
    _counter = 0
    last = {
        'tags': [],
        'source': '',
        'size': '',
        'uploader': '',
        'char': []
    }
    loop = asyncio.get_event_loop()
    tasklist = [req(link,heads) for link in links]
    future = asyncio.ensure_future(asyncio.wait(tasklist))
    loop.run_until_complete(future)
    # for link in links:
    #     print33(_counter, len(links), link)
    #     _counter += 1
    #     request = asyncio.create_task(req(link,heads))
    #     tasklist.append(request)

    i= _links
    for m in i:
        content = html.fromstring(m)
        copyright = content.xpath(
            '//*[@id="tag-list"]/li[@class="tag-type-copyright"]/a/text()')
        _source = ifempty(content.xpath(
            '//*[@id="tag-list"]/li[text()="Source: "]/a/@href'))[0]
        _size = ifempty(content.xpath(
            '//*[@id="tag-list"]/li[contains(text(),"Size: ")]/text()'))[0]
        _uploader = ifempty(content.xpath(
            '//*[@id="tag-list"]/li[contains(text(),"Posted: ")]/a/text()'))[0]
        _tags = content.xpath(
            '//*[@id="tag-list"]/li[@class="tag-type-general"]/a/text()')
        _char = content.xpath(
                '//*[@id="tag-list"]/li[@class="tag-type-character"]/a/text()')
        _ifcount = True
        if (_source, _size, _uploader,_char) == (last['source'], last['size'], last['uploader'], last['char']):
            _tags = getnotexist(_tags, last['tags'])
            _ifcount=False
        else: _ifcount=True
        if not(copyright[0:1]):
            if 'nocopyright' not in tags:
                tags['nocopyright'] = {}
                tags['nocopyright']['count'] = 0
                tags['nocopyright']['tags'] = []
            tags['nocopyright']['tags'].extend(_tags)
            if _ifcount: tags['nocopyright']['count'] += 1

        elif copyright[0] != 'original':
            chars = content.xpath(
                '//*[@id="tag-list"]/li[@class="tag-type-character"]/a/text()')
            for i in chars:
                if i not in tags:
                    tags[i] = {}
                    tags[i]['count'] = 0
                    tags[i]['tags'] = []
                tags[i]['tags'].extend(_tags)
                if _ifcount:tags[i]['count'] +=1

        else:
            if 'original' not in tags:
                tags['original'] = {}
                tags['original']['count'] = 0
                tags['original']['tags'] = []
            tags['original']['tags'].extend(_tags)
            if _ifcount:tags['original']['count']+=1

        (last['source'], last['size'], last['uploader'],
        last['tags'], last['char']) = (_source, _size, _uploader, _tags,_char)
    with open('./catch/gettags_' + str(math.floor(time.time())) + '.json','w',encoding='utf-8') as F:
        F.write(json.dumps(tags))
    return tags

# print (gettagsbycharacter('dilation_belt'))
