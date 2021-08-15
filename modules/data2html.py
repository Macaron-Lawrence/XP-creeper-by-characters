import math
import time
def renderpie(obj:dict,title:str,subtitle:str,name:str):
    html = ''
    temp = {}
    temp['text'] = '"'+title+'"'
    temp['subtext'] = '"'+subtitle+'"'
    temp['name'] = '"' + name +'"'
    temp['data'] = ''
    arr = obj[list(obj.keys())[0]]
    arr.sort(key=lambda k:k[1],reverse=True)
    for i in arr:
        temp['data']+='{value: '+ str(i[1]) +', name: "'+ i[0] +'"},'
    temp['data'] = temp['data'][:-1]
    with open('./templates/index.xml', 'r', encoding='utf-8') as f:
        html = f.read()
    for i in temp.keys():
        html = html.replace('{%=' + i + '%}',temp[i])
    with open('./html/'+ title +'_' + subtitle +'_'+ str(math.floor(time.time()))+ '.html','w',encoding='utf-8') as F:
        F.write(html)

