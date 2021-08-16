from lxml import html
import re
import requests
import json
import math
from modules.headers import headers
# from headers import headers
# +'+-rating%3A' + 'safe'
import time

heads = headers()
rating = '+-rating%3A' + 'safe'
host = 'https://gelbooru.com/index.php'
# keywords = 'arknights' + rating  # 关键词


def print33(indexnow, indextotal, title):  # 进度条
    A_count = math.floor(indexnow/indextotal*33)
    A = '#'*A_count
    B = '-'*(33-A_count)
    C = math.floor(indexnow/indextotal*1000)/10
    print('>> 正在抓取 |' + A + B + '| ' + str(C) + '% | ' + title, flush=True)


def getpagelinksbyid(id, url):  # 通过获取页面的links
    _request = requests.get(host + url + str(id),
                            headers=heads, timeout=(5, 60))
    _content = html.fromstring(_request.content)
    _links = _content.xpath('//*[@id="container"]/main/div[7]/article/a/@href')
    return _links


def getpagelinks(url):  # 获取页面的links
    _request = requests.get(url, headers=heads, timeout=(5, 60))
    _content = html.fromstring(_request.content)
    _links = _content.xpath('//*[@id="container"]/main/div[7]/article/a/@href')
    return _links


def getsearchids(terns, url):  # 获取搜索需要的最大id
    searched = []
    if terns != 0:
        for i in range(0, terns):
            _next = getpagelinksbyid((i+1)*19992, url)
            _next = re.search('(?<=(id=))\d+', _next[-1]).group()
            searched.append(_next)
    return searched


def getsearchs(keywords, terns, url):  # 获取搜索关键字
    searchids = getsearchids(terns, url)
    _keywords = []
    for i in range(0, len(searchids)+1):
        if not(searchids[0:1]):
            _keywords.append(keywords)
        else:
            if i == 0:
                _keywords.append(keywords + '+id:>' + searchids[i])
            elif searchids[i+1:i+2]:
                _keywords.append(keywords + '+id:<' +
                                 searchids[i] + '+id:>' + searchids[i+1])
            else:
                _keywords.append(keywords + '+id:<' + searchids[i-1])
    return _keywords


def getlinks(__keywords):  # 获取图片页链接
    keywords = __keywords# + rating
    url = '?page=post&s=list&tags='+keywords+'&pid='
    request = requests.get(host + url + '0', headers=heads, timeout=(5, 60))
    content = html.fromstring(request.content)
    lastpage = content.xpath('//div[@id="paginator"]/a[last()]/@href')[0]
    lastpageid = re.search('(?<=(pid=))\d+', lastpage).group(0)
    terns = int(lastpageid)//19992

    searches = getsearchs(keywords, terns, url)
    s_links = []
    _links = {
        'keywords': __keywords,
        'links': []
    }
    _counter = 0
    for i in searches:
        _request = requests.get(host + '?page=post&s=list&tags=' +
                                i + '&pid=' + '0', headers=heads, timeout=(5, 60))
        _content = html.fromstring(_request.content)
        _lastpage = _content.xpath('//div[@id="paginator"]/a[last()]/@href')[0]
        _lastpageid = re.search('(?<=(pid=))\d+', _lastpage).group(0)
        for n in range(0, (int(_lastpageid)//42)+1):
            s_links.append(host + '?page=post&s=list&tags=' +
                           str(i) + '&pid=' + str(n*42))
    for m in s_links:
        print33(_counter, len(s_links), m)
        _links['links'].extend(getpagelinks(m))
        _counter += 1
    with open('./catch/getlinks_'+ str(math.floor(time.time())) +'.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(_links))

    return _links

# getlinks('forced_orgasm')
