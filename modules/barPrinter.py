import math


def print33(indexnow, indextotal, title):  # 进度条
    A_count = math.floor(indexnow/indextotal*33)
    A = '#'*A_count
    B = '-'*(33-A_count)
    C = math.floor(indexnow/indextotal*1000)/10
    print('>> 正在抓取 |' + A + B + '| ' + str(C) + '% | ' + title, flush=True)
