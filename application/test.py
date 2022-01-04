# -*- coding:utf-8 -*-


import requests
import json

'''
    测试端程序
'''

if __name__ == '__main__':

    # ip_port = 'http://180.76.242.135:10200/test?'
    # ip_port = 'http://10.3.74.139:10200/test?'
    ip_port = 'http://ip:port/test?'

    # str1 = 'like all the others from the maker of this brand.'
    str1 = 'articles from countries;'
    url = ip_port + 'str1=' + str1
    res = requests.get(url)
    print(res.text)


