#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:38:03 2018

@author: little-frog
"""
from urllib.parse import urlencode###构造url的函数
import requests
import time
import json

base_url = 'https://m.weibo.cn/api/container/getIndex?'###微博个人主页公用地址
path = 'result.txt'
headers = {
    'Host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/p/1005051496852380',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}
def get_page(page):###其中的params需要依照要爬取的Ajax进行填写
    params = {
        'containerid':'1076031496852380',
        'page':page
    }
    url = base_url + urlencode(params)###用于构造url
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.json()###返回json格式的数据
    except requests.ConnectionError as e:
        print('Error',e.args)
###定义解析方法
from pyquery import PyQuery as pq

def parse_page(json):
    res=[]
    if json:
        items = json.get('data').get('cards')###json数据类型为dict，用get的好处就是如果没有值就返回空而不会报错
        for item in items:###item有多个元素
            item = item.get('mblog')
            if item:###item有None，不加这玩意儿会报错
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments_count'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                yield weibo###构成一个迭代器

if __name__ == '__main__':
    for page in range(1,6):###想爬多少页完全看个人心情
        res = get_page(page)
        results = parse_page(res)
        for result in results:
            #print(result)###也可以改写为with open+write来输出数据
            with open (path,'a',encoding='utf-8') as f:
                f.write(json.dumps(result,ensure_ascii=False)+'\n')
        time.sleep(1)###加这玩意儿，免得爬太勤快被封了