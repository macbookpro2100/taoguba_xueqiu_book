# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool  # 多线程并行库

from src.tools.config import Config
from src.tools.debug import Debug


class Control(object):
    thread_pool = ThreadPool(Config.max_thread)

    @staticmethod
    def control_center(argv, test_flag):
        max_try = Config.max_try
        for time in range(max_try):
            if test_flag:
                if Config.debug:
                    Control.debug_control(argv)
                else:
                    Control.release_control(argv)
                    # Control.thread_pool.map(**argv)
        return

    @staticmethod
    def debug_control(argv):
        for item in argv['iterable']:
            argv['function'](item)
        return

    @staticmethod
    def release_control(argv):
        try:
            for item in argv['iterable']:
                argv['function'](item)
            return
        except Exception as e:
            # 按照惯例，报错全部pass掉
            # 等用户反馈了再开debug查吧
            Debug.logger.debug(e.message)
            pass
        return