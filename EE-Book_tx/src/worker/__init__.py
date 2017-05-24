#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zhihu_worker import (QuestionWorker, AuthorWorker, CollectionWorker,
                          TopicWorker, ColumnWorker)
from sinablog_worker import sinablogAuthorWorker
from jianshu_worker import JianshuAuthorWorker
from jianshu_worker import JianshuCollectionWorker
from jianshu_worker import JianshuNotebooksWorker
from csdnblog_worker import csdnAuthorWorker
from cnblogs_worker import CnblogsAuthorWorker
from yiibai_worker import YiibaiWorker
from talkpython_worker import TalkPythonWorker
from taoguba_worker import taogubaAuthorWorker
from xueqiu_worker import xueqiuAuthorWorker


def worker_factory(task):
    type_list = {
        'answer': QuestionWorker,
        'question': QuestionWorker,
        'author': AuthorWorker,
        'collection': CollectionWorker,
        'topic': TopicWorker,
        'column': ColumnWorker,
        'article': ColumnWorker,
        'sinablog_author': sinablogAuthorWorker,
        'taoguba_author': taogubaAuthorWorker,
        'xueqiu_author': xueqiuAuthorWorker,
        'cnblogs_author': CnblogsAuthorWorker,
        'jianshu_author': JianshuAuthorWorker,
        'jianshu_collection': JianshuCollectionWorker,
        'jianshu_notebooks': JianshuNotebooksWorker,
        'csdnblog_author': csdnAuthorWorker,
        'yiibai': YiibaiWorker,
        'talkpython': TalkPythonWorker,
    }
    for key in task:
        worker = type_list[key](task[key])
        worker.start()
    return
