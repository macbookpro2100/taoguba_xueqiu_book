# -*- coding: utf-8 -*-
import re

from getpass import getpass


# 删掉?
def set_account(recipe_kind):
    u"""
    different login process, depending on the type
    :param recipe_kind:
    :return:
    """
    from tools.debug import Debug
    if recipe_kind == 'zhihu':
        print(u"登录知乎中...")
        print(u"请输入注册账号,回车确认")
        account = raw_input()
        if account:
            while not re.search(r'\w+@[\w\.]{3,}', account):
                print u'抱歉，输入的账号不规范...\n请输入正确的知乎登录邮箱\n'
                print u'请重新输入账号，回车确认'
                account = raw_input()
            password = getpass(u'请输入密码，回车确认:')
            while len(password) < 6:
                print u'密码长度不正确，密码至少6位'
                print u'请重新输入密码，回车确认'
                password = raw_input()
        else:
            account, password = set_account(recipe_kind)
    else:
        Debug.logger.error(u"出错了!!!,目前需要登录的只有知乎")
        import sys
        sys.exit()
    return account, password


def set_picture_quality():
    print u'图片模式为1'
    try:
        # quality = int(raw_input())
        quality = 1
    except ValueError as error:
        print error
        print u'数字转换错误。。。'
        print u'图片模式重置为标准模式，点击回车继续'
        quality = 1
        raw_input()
    if not (quality in [0, 1, 2]):
        print u'输入数值非法'
        print u'图片模式重置为标准模式，点击回车继续'
        quality = 1
        raw_input()
    return quality
