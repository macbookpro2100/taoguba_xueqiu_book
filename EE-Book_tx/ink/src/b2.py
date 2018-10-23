# -*- coding: UTF-8 -*-
import requests
from contextlib import closing
import sys  # 修改默认编码
import os  # 添加系统路径


class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # [名称] 状态 进度 单位 分割线 总数 单位
        _info = self.info % (
            self.title, self.status, self.count / self.chunk_size, self.unit, self.seq, self.total / self.chunk_size,
            self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
            print(self.__get_info(), end_str)


from multiprocessing import Process, Queue

import time
from lxml import etree
import requests


class BuffettSpider(Process):
    def __init__(self, url, q, path):
        # 重写写父类的__init__方法
        super(BuffettSpider, self).__init__()
        self.url = url
        self.q = q
        self.filePath = path

    def run(self):
        self.do_action()

    def do_action(self):
        '''
        xiazai网站
        :return:
        '''
        url = self.url
        urlll = url.split('/')[-1]
        filename = urlll.split('?')[0]
        dstfile = '{}/{}'.format(self.filePath, filename)

        with closing(requests.get(url, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                print('文件大小:%0.2f KB' % (content_size / chunk_size))
                progress = ProgressBar("%s下载进度" % filename
                                       , total=content_size
                                       , unit="KB"
                                       , chunk_size=chunk_size
                                       , run_status="正在下载"
                                       , fin_status="下载完成")

                with open(dstfile, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        progress.refresh(count=len(data))
            else:
                # 创建异常连接列表
                print('下载 异常  '.format(url))
                # 链接地址 目标dir  May index out of List
                erroeLine = "{}|{}\n".format(url, dstfile)
                ff = open('failed.txt', 'a+')
                ff.write(erroeLine)

                ff.close()

        self.q.put("下载了" + "\t" + dstfile)
def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print "---  new folder...  ---"
        print "---  OK  ---"

    else:
        print "---  There is this folder!  ---"


def main():
    # 创建一个队列用来保存进程获取到的数据

    file_name = 'b2.txt'
    try:
        with open(file_name, 'r') as read_list:
            read_list = read_list.readlines()

            resultsL = read_list.__len__()
            for x in range(0, resultsL):
                line = read_list[x]
                splits = line.split('#')
                firestIndex = (int)(splits[0])
                lastIndex = (int)(splits[1])
                base_url = splits[-1]
                # basePath = '/FileList/2018/b{}'.format(x)
                basePath = '/FileList/2018/b2018'

                # 创建文件夹
                mkdir(basePath)

                #分解Queue 太多会导致 https连接数过多 faied connect

                spledBASE = 10
                splitFile = (int)(lastIndex / spledBASE)


                stttaarrd  = 70
                # stttaarrd  = (int)(firestIndex / spledBASE)

                for page in range(stttaarrd,splitFile):
                    startpage = 1 + page * spledBASE
                    endpage = spledBASE + 1 + page * spledBASE
                    # endpage = 400
                    q = Queue()
                    url_list = [base_url.format(num) for num in range(startpage, endpage)]

                    Thread_list = []

                    for url in url_list:
                        p = BuffettSpider(url, q, basePath)
                        p.start()
                        Thread_list.append(p)

                    for i in Thread_list:
                        i.join()

                    while not q.empty():
                        print q.get()

                        # 保存文件

    except IOError as e:
        print(u"\nOops! No " + file_name + ". creating " + file_name + "...")
        with open(file_name, 'w') as read_list:
            read_list.close()
        sys.exit()


if __name__ == "__main__":
    start = time.time()
    main()
    print '[info]耗时：%s' % (time.time() - start)