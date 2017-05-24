# -*- coding: utf-8 -*-
import cookielib
import os
import urllib2
import sys

from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedLoginException
from tools.extra_tools import ExtraTools
from tools.path import Path


class Login(object):
    def __init__(self, recipe_kind, from_ui=False):
        # TODO: from_ui
        self.recipe_kind = recipe_kind
        self.from_ui = from_ui

    def start(self):
        try:
            client = ZhihuClient()
            client.login_in_terminal()
            client.save_token(Path.ZHIHUTOKEN)
        except NeedLoginException:
            print u"Oops, please try again."
            sys.exit()
        return

