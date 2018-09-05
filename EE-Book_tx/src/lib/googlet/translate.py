#!/usr/bin/python
#coding:utf-8
import requests, execjs, json, sys
from CalcTk import CalcTk
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
headers = {
'Host': 'translate.google.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
'Referer': 'https://translate.google.cn/',
'Cookie': 'NID=101=pkAnwSBvDm2ACj2lEVnWO7YEPUoWCTges7B7z2jJNyrNwAZ2OL9FFOQLpdethA_20gCVqukiHnVm1hUbMGZc_ItQFdP5AHoq5XoMeEORaeidU196NDVRsrAu_zT0Yfsd; _ga=GA1.3.1338395464.1492313906',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0'
}

params = {
'client': 't', 'sl': 'en', 'tl': 'zh-CN', 'hl': 'zh-CN',
'dt': 'at', 'dt': 'bd', 'dt': 'ex', 'dt': 'ld', 'dt': 'md',
'dt': 'qca', 'dt': 'rw', 'dt': 'rm', 'dt': 'ss', 'dt': 't',
'ie': 'UTF-8', 'oe': 'UTF-8', 'source': 'bh', 'ssel': '0',
'tsel': '0', 'kc': '1', 'tk': '376032.257956'
}

TK = CalcTk()

def get_res(url, data, params):
    try:
        res = requests.post(url, headers = headers, data = data, params = params, timeout = 2)
        res.raise_for_status()
        return res
    except Exception as ex:
        print('[-]ERROR: ' + str(ex))
        return res
        
def parse_json(res):
    return json.loads(res)

def translate(text):
    global params, TK
    url = 'https://translate.google.cn/translate_a/single'
    data = {'q': text}
    try:
        params['tk'] = TK.get_tk(text)
        res = get_res(url, data, params)
        ret_list = parse_json(res.text)
        return ret_list[0]
    except Exception as ex:
        print('[-]ERROR: ' + str(ex))
        return None


def main():
    source = 'indx.txt'
    target = 'index.txt'
    lines = []
    # if len(sys.argv) == 3:
    #     source = sys.argv[1]
    #     target = sys.argv[2]
    # elif len(sys.argv) == 2:
    #     source = sys.argv[1]
    #     target = 'T_' + source
    # else:
    #     print('[-]ERROR: \nUsage: python translate.py sourceFile [targetFile]')
    #     return
    
    try:
        english = u"Salmonella infection triggers multiple inflammatory pathways, suchas stimulationof Toll-like receptor (TLR) signaling via TLR4-mediated sensing of bacterial LPSs as well as recognition of flagellin by TLR5. Furthermore, bacterial peptidoglycan can be sensed via nucleotide-binding and oligomerization domain (NOD) receptors in the host cytosol. Addi-tional evidence further demonstrates that bacterial effector-mediated Rho GTPase activation contributes to NF-kB signaling. Interestingly, our data revealed a prominent increase in numerous ubiquitination sites of linear (methionine (M1)-linked) Ub chain assembly complex (LUBAC) subunits upon infection."
        ret = translate(english)
        if not ret:
            raise Exception('Empty Response')
        for item in ret:
            print ('{}\n{}\n'.format(item[1], item[0]))

        # english.close()
    except Exception as ex:
        print('[-]ERROR: ' + str(ex))
        return
    

    print('[+]翻译完成')
    

if __name__ == '__main__':
    main()
