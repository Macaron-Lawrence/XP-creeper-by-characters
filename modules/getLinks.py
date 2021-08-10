from lxml import html
from typing import Text
import re
import requests
import json
import math

keywords = 'arknights'
# +'+-rating%3A' + 'safe'

def print33(indexnow,indextotal,title):
    A_count = math.floor(indexnow/indextotal*33)
    A = '#'*A_count
    B = '-'*(33-A_count)
    C = math.floor(indexnow/indextotal*1000)/10

    print('>> 正在抓取 |' + A + B + '| '+ str(C) + '% | ' + title,flush=True)


def getpagelinks(id,host,url,heads):
    _request = requests.get(host + url + str(id), headers = heads, timeout=(5,20))
    _content = html.fromstring(_request.content)
    _links = _content.xpath('//*[@id="container"]/main/div[7]/article/a/@href')
    return _links

def getsearchids(terns,host,url,heads):
    searched = []
    if terns !=0:
        for i in range(0,terns):
            _next = getpagelinks((i+1)*19992,host,url,heads)
            _next = re.search('(?<=(id=))\d+',_next[-1]).group()
            searched.append(_next)
    return searched

def getsearchs(keywords,terns,host,url,heads):
    searchids = getsearchids(terns,host,url,heads)
    _keywords = []
    for i in range(0,len(searchids)+1):
        if not(searchids[0:1]):
            _keywords.append(keywords)
        else:
            if i == 0:
                _keywords.append(keywords + '+id:>' + searchids[i])
            elif searchids[i+1:i+2]:
                _keywords.append(keywords + '+id:<' + searchids[i] + '+id:>' + searchids[i+1])
            else:
                _keywords.append(keywords + '+id:<' + searchids[i-1])
    return _keywords

def getlinks(keywords):
    heads = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'PHPSESSID': 'rmhsof5bmdujqv6qhodr7ccbt2; comment_threshold=0; post_threshold=0; fringeBenefits=yup'
    }
    rating = '+-rating%3A' + 'safe'
    host = 'https://gelbooru.com/index.php'
    url = '?page=post&s=list&tags='+keywords+'&pid='
    request = requests.get(host + url + '0', headers = heads, timeout=(5,20))
    content = html.fromstring(request.content)
    lastpage = content.xpath('//div[@id="paginator"]/a[last()]/@href')[0]
    lastpageid = re.search('(?<=(pid=))\d+', lastpage).group(0)
    terns = int(lastpageid)//19992

    searches = getsearchs(keywords,terns,host,url,heads)
    s_links = []
    _links = {
        'keywords':keywords,
        'links' :[]
    }
    _counter = 0
    for i in searches:
        _request = requests.get(host + '?page=post&s=list&tags=' + i + '&pid=' + '0', headers = heads, timeout=(5,20))
        _content = html.fromstring(_request.content)
        _lastpage = _content.xpath('//div[@id="paginator"]/a[last()]/@href')[0]
        _lastpageid = re.search('(?<=(pid=))\d+', _lastpage).group(0)
        for n in range(0,(int(_lastpageid)//42)+1):
            s_links.append(host + '?page=post&s=list&tags=' + str(i) + '&pid=' + str(n*42))
    for m in s_links:
        print33(_counter,len(s_links),m)
        __request = requests.get(m,headers = heads, timeout=(5,20))
        __content = html.fromstring(__request.content)
        _links['links'].extend(__content.xpath('//*[@id="container"]/main/div[7]/article/a/@href'))
        _counter +=1
    with open('./links.json','w',encoding='utf-8') as file:
        file.write(json.dumps(_links))

getlinks(keywords)
