# -*- coding: utf-8 -*-
from src.container.task import QuestionTask, AnswerTask, AuthorTask, CollectionTask, TopicTask, \
    ArticleTask, ColumnTask, WechatTask,HuaWeiTask,HuXiuTask,ZhengshitangTask,XueQiuTask,SinaTask,WuXiaTask,JinWanKanShaTask,Doc360Task,TodoTask,Todo1Task,Todo2Task
from src.tools.debug import Debug
from src.tools.match import Match
from src.tools.type import Type


class CommandParser(object):
    u"""
    通过Parser类，生成任务列表,以task容器列表的形式返回回去
    """

    @staticmethod
    def get_task_list(command):
        u"""
        解析指令类型
        """
        command = command \
            .replace(' ', '') \
            .replace('\r', '') \
            .replace('\n', '') \
            .replace('\t', '') \
            .split('#')[0]
        command_list = command.split('$')

        task_list = []
        for command in command_list:
            task = CommandParser.parse_command(command)
            if not task:
                continue
            task_list.append(task)
        return task_list

    @staticmethod
    def detect(command):
        for command_type in [
            Type.answer, Type.question,
            Type.author, Type.collection, Type.topic,
            Type.article, Type.column,  # 文章必须放在专栏之前（否则检测类别的时候就一律检测为专栏了）
            Type.wechat,
            Type.huxiu, Type.huawei, Type.sina, Type.zhengshitang, Type.xueqiu,Type.wuxia,Type.jinwankansa,
            Type.doc360,Type.todo,Type.todo1,Type.todo2
        ]:
            result = getattr(Match, command_type)(command)
            if result:
                return command_type
        return Type.unknown

    @staticmethod
    def parse_command(raw_command=''):
        u"""
        分析单条命令并返回待完成的task
        """
        parser = {
            Type.author: CommandParser.parse_author,
            Type.answer: CommandParser.parse_answer,
            Type.question: CommandParser.parse_question,
            Type.collection: CommandParser.parse_collection,
            Type.topic: CommandParser.parse_topic,
            Type.article: CommandParser.parse_article,
            Type.column: CommandParser.parse_column,
            Type.wechat: CommandParser.parse_wechat,
            Type.huxiu: CommandParser.parse_huxiu,
            Type.huawei: CommandParser.parse_huawei,
            Type.sina: CommandParser.parse_sina,
            Type.zhengshitang: CommandParser.parse_zhengshitang,
            Type.xueqiu: CommandParser.parse_xueqiu,
            Type.wuxia: CommandParser.parse_wuxia,
            Type.jinwankansa: CommandParser.parse_jinwankansa,
            Type.doc360: CommandParser.parse_doc360,
            Type.todo: CommandParser.parse_todo,
            Type.todo1: CommandParser.parse_todo1,
            Type.todo2: CommandParser.parse_todo2,
            Type.unknown: CommandParser.parse_error,
        }
        kind = CommandParser.detect(raw_command)
        return parser[kind](raw_command)

    @staticmethod
    def parse_question(command):
        result = Match.question(command)
        question_id = result.group(u'question_id')
        task = QuestionTask(question_id)
        return task

    @staticmethod
    def parse_answer(command):
        result = Match.answer(command)
        question_id = result.group(u'question_id')
        answer_id = result.group(u'answer_id')
        task = AnswerTask(question_id, answer_id)
        return task

    @staticmethod
    def parse_author(command):
        result = Match.author(command)
        author_page_id = result.group(u'author_page_id')
        task = AuthorTask(author_page_id)
        return task

    @staticmethod
    def parse_collection(command):
        result = Match.collection(command)
        collection_id = result.group(u'collection_id')
        task = CollectionTask(collection_id)
        return task

    @staticmethod
    def parse_topic(command):
        result = Match.topic(command)
        topic_id = result.group(u'topic_id')
        task = TopicTask(topic_id)
        return task

    @staticmethod
    def parse_article(command):
        result = Match.article(command)
        column_id = result.group(u'column_id')
        article_id = result.group(u'article_id')
        task = ArticleTask(column_id, article_id)
        return task

    @staticmethod
    def parse_column(command):
        result = Match.column(command)
        column_id = result.group(u'column_id')
        task = ColumnTask(column_id)
        return task

    @staticmethod
    def parse_wechat(command):
        result = Match.wechat(command)
        account_id = result.group(u'account_id')
        task = WechatTask(account_id)
        return task

    @staticmethod
    def parse_huxiu(command):
        result = Match.huxiu(command)
        account_id = result.group(u'huxiu_id')
        task = HuXiuTask(account_id)
        return task

    @staticmethod
    def parse_huawei(command):
        result = Match.huawei(command)
        account_id = result.group(u'haccount_id')
        task = HuaWeiTask(account_id)
        return task
    @staticmethod
    def parse_sina(command):
        result = Match.sina(command)
        account_id = result.group(u'sinablog_people_id')
        task = SinaTask(account_id)
        return task
    @staticmethod
    def parse_xueqiu(command):
        result = Match.xueqiu(command)
        account_id = result.group(u'xueqiu_author_id')
        task = XueQiuTask(account_id)
        return task
    @staticmethod
    def parse_zhengshitang(command):
        result = Match.zhengshitang(command)
        account_id = result.group(u'account_id')
        task = ZhengshitangTask(account_id)
        return task
    @staticmethod
    def parse_wuxia(command):
        result = Match.wuxia(command)
        account_id = result.group(u'account_id')
        task = WuXiaTask(account_id)
        return task

    @staticmethod
    def parse_jinwankansa(command):
        result = Match.jinwankansa(command)
        account_id = result.group(u'account_id')
        task = JinWanKanShaTask(account_id)
        return task
    @staticmethod
    def parse_doc360(command):
        result = Match.doc360(command)
        account_id = result.group(u'account_id')
        task = Doc360Task(account_id)
        return task
    @staticmethod
    def parse_todo(command):
        result = Match.todo(command)
        account_id = result.group(u'account_id')
        task = TodoTask(account_id)
        return task
    @staticmethod
    def parse_todo1(command):
        result = Match.todo1(command)
        account_id = result.group(u'account_id')
        task = Todo1Task(account_id)
        return task
    @staticmethod
    def parse_todo2(command):
        result = Match.todo2(command)
        account_id = result.group(u'account_id')
        task = Todo2Task(account_id)
        return task

    @staticmethod
    def parse_error(command):
        if command:
            Debug.logger.info(u"""无法解析记录:{}所属网址类型,请检查后重试。""".format(command))
        return
