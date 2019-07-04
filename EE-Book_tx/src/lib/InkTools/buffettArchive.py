# coding: utf-8
import requests
from contextlib import closing
import sys  # 修改默认编码
import os  # 添加系统路径
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
import gevent
import requests
import urlparse
import os
import time


class Downloader:
    def __init__(self, pool_size, retry=12):
        self.pool = Pool(pool_size)
        self.session = self._get_http_session(pool_size, pool_size, retry)
        self.retry = retry
        self.dir = ''
        self.succed = {}
        self.failed = []
        self.ts_total = 0

    def _get_http_session(self, pool_connections, pool_maxsize, max_retries):
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize,
                                                max_retries=max_retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def run(self, m3u8_url, dir=''):
        self.dir = dir
        if self.dir and not os.path.isdir(self.dir):
            os.makedirs(self.dir)

        r = self.session.get(m3u8_url, timeout=10)
        if r.ok:
            body = r.content
            if body:
                ts_list = [urlparse.urljoin(m3u8_url, n.strip()) for n in body.split('\n') if
                           n and not n.startswith("#")]
                ts_list = zip(ts_list, [n for n in xrange(len(ts_list))])
                if ts_list:
                    self.ts_total = len(ts_list)
                    print self.ts_total
                    g1 = gevent.spawn(self._join_file)
                    self._download(ts_list)
                    g1.join()
        else:
            print r.status_code

    def _download(self, ts_list):
        self.pool.map(self._worker, ts_list)
        if self.failed:
            ts_list = self.failed
            self.failed = []
            self._download(ts_list)

    def _worker(self, ts_tuple):
        url = ts_tuple[0]
        index = ts_tuple[1]
        retry = self.retry
        while retry:
            try:
                r = self.session.get(url, timeout=20)
                if r.ok:
                    file_name = url.split('/')[-1].split('?')[0]
                    print file_name
                    with open(os.path.join(self.dir, file_name), 'wb') as f:
                        f.write(r.content)
                    self.succed[index] = file_name
                    return
            except:
                retry -= 1
        print '[FAIL]%s' % url
        self.failed.append((url, index))

    def _join_file(self):
        index = 0
        outfile = ''
        while index < self.ts_total:
            file_name = self.succed.get(index, '')
            if file_name:
                infile = open(os.path.join(self.dir, file_name), 'rb')
                if not outfile:
                    outfile = open(os.path.join(self.dir, file_name.split('.')[0] + '_all.' + file_name.split('.')[-1]),
                                   'wb')
                outfile.write(infile.read())
                infile.close()
                os.remove(os.path.join(self.dir, file_name))
                index += 1
            else:
                time.sleep(1)
        if outfile:
            outfile.close()


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print "---  new folder...  ---"
        print "---  OK  ---"

    else:
        print "---  There is this folder!  ---"


if __name__ == '__main__':

    file_name = 'ReadList.txt'
    try:
        with open(file_name, 'r') as read_list:
            read_list = read_list.readlines()

            resultsL = read_list.__len__()
            for x in range(0, resultsL):
                line = read_list[x]
                splits = line.split('#')
                fieName = (str)(splits[0])



                base_url = splits[1]

                print base_url

                basePath = '/FileList/2018/{}'.format(fieName)

                # 创建文件夹
                mkdir(basePath)
                downloader = Downloader(50)
                # base_url = 'https://cnbcmbr-vh.akamaihd.net/i/mp4/VCPS/Y2018/M04D06/7000011888/2017-BAM-2v2_MBR_,0240,0300,0500,0700,0900,1300,1700,4500,.mp4.csmil/index_7_av.m3u8'
                downloader.run(base_url, basePath)



    except IOError as e:
        print(u"\nOops! No " + file_name + ". creating " + file_name + "...")
        with open(file_name, 'w') as read_list:
            read_list.close()
        sys.exit()
