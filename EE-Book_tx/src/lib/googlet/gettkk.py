#!/usr/bin/python
#coding:utf-8
import requests, re, execjs

def get_res(url):
    try:
        res = requests.get(url, timeout = 1.5)
        res.raise_for_status()
        #res.encoding = 'utf-8'
        return res
    except Exception as ex:
        print('[-]ERROR: ' + str(ex))
        return res

def find_tkk_fn(res):
    re_tkk = r"TKK=eval\('(\(\(function\(\)\{.+?\}\)\(\)\))'\);"
    tkk_fn = re.search(re_tkk, res)
    return tkk_fn

def get_tkk():
    url = 'https://translate.google.cn/'
    try:
        res = get_res(url)
        tkk_fn = find_tkk_fn(res.text)
        content = tkk_fn.group(1).encode('utf-8').decode('unicode_escape')
        tkk = execjs.eval(content)
        return tkk
    except Exception as ex:
        print(ex)
    
