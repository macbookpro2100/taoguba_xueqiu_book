# -*- coding: utf-8 -*-
import json
import os

from path import Path


class Config(object):
    u"""
    用于储存、获取设置值、全局变量值
    """
    # 全局变量
    update_time = '2016-03-07'  # 更新日期

    debug = False
    now_id = ''


    need_account = True        # 是否需要账号密码
    login_with_previously_config = True  # 是否通过之前的登陆记录进行登陆

    account = 'zhihu2ebook@hotmail.com'  # 默认账号密码
    # password = 'Zhihu2Ebook'
    remember_account_set = False    # 是否使用已有密码
    max_thread = 20             # 最大线程数
    picture_quality = 1         # 图片质量（0/1/2，无图/标清/原图）
    max_question = 100          # 每本电子书中最多可以放多少个问题
    max_answer = 6000            # 每本电子书中最多可以放多少个回答
    max_article = 600           # 每本电子书中最多可以放多少篇文章
    max_try = 5                 # 最大尝试次数
    answer_order_by = 'agree_count'         # 问题答案排序原则  agree_count|update_date|char_count
    answer_order_by_desc = True             # 问题答案排序顺序->是否为desc
    question_order_by = 'agree_count'       # 问题排序原则  agree_count|char_count|answer_count
    question_order_by_desc = True           # 问题排序顺序->是否为desc
    article_order_by = 'update_date'        # 文章排序原则  update_date|agree_count|char_count
    author_answer_order_by = 'agree_count'  # 作者回答排序原则  agree_count|answer_id|char_count
    author_answer_order_by_desc = True      # 作者回答排序原则->是否为desc
    article_order_by_desc = False           # 文章排序顺序->是否为desc
    show_private_answer = True
    timeout_download_picture = 10           # 多给知乎服务器点时间，批量生成tex太痛苦了- -
    timeout_download_html = 5
    sql_extend_answer_filter = 'and content > '' '  # 附加到answer_sql语句后，用于对answer进行进一步的筛选（示例: and(agree > 5) ）

    @staticmethod
    def _save():
        with open(Path.config_path, 'w') as f:
            data = dict((
                (key, Config.__dict__[key]) for key in Config.__dict__ if '_' not in key[:2]
            ))
            json.dump(data, f, indent=4)
        return

    @staticmethod
    def _load():
        if not os.path.isfile(Path.config_path):
            return
        with open(Path.config_path) as f:
            config = json.load(f)
            if not config.get('remember_account_set'):
                # 当选择不记住密码时，跳过读取，使用默认设置
                # 不考虑用户强行在配置文件中把account改成空的情况
                return
        for (key, value) in config.items():
            setattr(Config, key, value)
        return
