#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import sys  # 修改默认编码
import os  # 添加系统路径

from src.exception import UnsupportTypeException
from src.TGBmain import TEEBook
from src.tools.config import Config
from src.tools.debug import Debug
from src.constants import __version__
from src.utils import log
from src.tools.match import Match
from src.login import Login
from src.constants import url_info

reload(sys)
base_path = unicode(os.getcwd())

# Python早期版本可以直接用sys.setdefaultencoding('utf-8')，新版本需要先reload一下
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(100000)  # 为BS解析知乎上的长答案增加递归深度限制


def main():
    file_name = 'ReadList.txt'
    log.print_log(u'read from %s' % file_name)

    counter = 1
    try:
        with open(file_name, 'r') as read_list:
            read_list = read_list.readlines()
            line = read_list[0]
            split_url = line.split('#')[0]

            recipe_kind = Match.get_website_kind(split_url)
            print recipe_kind
            counter += 1
            if recipe_kind == 'Unsupport type':
                print('Unsupported website or url type. \nPlease check url.')
                sys.exit()
    except IOError as e:
        print(u"\nOops! No " + file_name + ". creating " + file_name + "...")
        with open(file_name, 'w') as read_list:
            read_list.close()
        sys.exit()
    except IndexError:
        if 1 == counter:
            print(u"\nOops! No content in " + file_name + u". Please check it out.")
            sys.exit()

    print(u"website type:" + str(recipe_kind))
    game = TEEBook(recipe_kind=recipe_kind, url=None, read_list=file_name)
    game.begin()
    sys.exit()


if __name__ == '__main__':
    main()
