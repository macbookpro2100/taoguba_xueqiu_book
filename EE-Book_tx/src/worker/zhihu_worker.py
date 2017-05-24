#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import datetime

from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedLoginException

from ..tools.db import DB
from ..tools.http import Http
from ..tools.match import Match
from ..tools.path import Path

from page_worker import PageWorker


client = ZhihuClient()

__all__ = [
    "QuestionWorker",
    "AuthorWorker",
    "CollectionWorker",
    "TopicWorker",
    "ColumnWorker",
]


def _client_load_token():
    try:
        client.load_token(Path.pwd_path + str(u'/ZHIHUTOKEN.pkl'))
    except IOError:
        print u"没有找到登录信息文件，请先登录"
        sys.exit()
    except NeedLoginException:
        print u"登录信息过期，请重新登录"
        sys.exit()


def get_answer_dict(answer={}, item=None):
    answer['author_id'] = item.author.id    # 如果用 item.author.id, 存的是 hash 值
    # 所以,目前 Author 部分不能用
    answer['author_sign'] = item.author.headline
    answer['author_logo'] = item.author.avatar_url
    answer['author_name'] = item.author.name
    answer['agree'] = item.voteup_count
    answer['content'] = u"<p>" + str(item.content) + u"</p>"
    answer['question_id'] = item.question.id
    answer['answer_id'] = item.id
    answer['commit_date'] = datetime.datetime.utcfromtimestamp(item.created_time).strftime("%Y-%m-%d")
    answer['edit_date'] = datetime.datetime.utcfromtimestamp(item.updated_time).strftime("%Y-%m-%d")
    answer['comment'] = item.comment_count
    answer['no_record_flag'] = 0   # TOD
    answer['href'] = u"https://www.zhihu.com/question/{0}/answer/{1}".format(answer['question_id'],
                                                                             answer['answer_id'])


class QuestionWorker(PageWorker):
    question_id = None
    question_oauth = None

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        _client_load_token()
        self.question_id = Match.question(target_url).group('question_id')
        self.info_url_complete_set.add(target_url)
        self.catch_content()

    def catch_content(self):
        self.question_oauth = client.question(int(self.question_id))
        question = dict()
        question['question_id'] = self.question_oauth.id
        question['title'] = self.question_oauth.title

        self.question_list += [question]

        for item in self.question_oauth.answers:
            answer = dict()
            # 如果用 item.author.id, 存的是 hash 值, 需要改 zhihu-oauth 的源码解决
            get_answer_dict(answer=answer, item=item)
            self.answer_list += [answer]

    def create_work_set(self, target_url):
        pass


class AuthorWorker(PageWorker):

    author_id = None
    people_oauth = None

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        _client_load_token()
        self.author_id = Match.author(target_url).group('author_id')
        self.people_oauth = client.people(self.author_id)
        info = dict()

        # info['hash'] = self.people_oauth.id
        info['name'] = self.people_oauth.name
        info['author_id'] = self.people_oauth.id   # zhihu-oauth, issues #4
        info['sign'] = self.people_oauth.headline
        info['logo'] = self.people_oauth.avatar_url
        info['description'] = self.people_oauth.description
        info['weibo'] = self.people_oauth.sina_weibo_url
        info['gender'] = self.people_oauth.gender
        info['asks'] = self.people_oauth.question_count
        info['answers'] = self.people_oauth.answer_count
        info['posts'] = self.people_oauth.articles_count
        info['agree'] = self.people_oauth.voteup_count
        info['thanks'] = self.people_oauth.thanked_count
        info['followee'] = self.people_oauth.following_count
        info['follower'] = self.people_oauth.follower_count
        info['followed_column'] = self.people_oauth.following_column_count
        info['followed_topic'] = self.people_oauth.following_topic_count
        self.info_list.append(info)
        self.info_url_complete_set.add(target_url)

        self.catch_content()
        return

    def catch_content(self):
        for item in self.people_oauth.answers:
            answer = dict()
            question = dict()
            get_answer_dict(answer=answer, item=item)
            question['question_id'] = item.question.id
            question['title'] = item.question.title
            self.answer_list += [answer]
            self.question_list += [question]

    def create_save_config(self):
        config = {
            'Answer': self.answer_list,
            'Question': self.question_list,
            'AuthorInfo': self.info_list,
        }
        return config

    def create_work_set(self, target_url):
        pass


class CollectionWorker(PageWorker):
    collection_index_list = []
    collection_id = None
    collection_oauth = None

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        _client_load_token()
        self.collection_id = Match.collection(target_url).group('collection_id')
        self.collection_oauth = client.collection(int(self.collection_id))
        info = dict()
        info['title'] = self.collection_oauth.title
        info['collection_id'] = self.collection_oauth.id
        info['follower'] = self.collection_oauth.follower_count
        info['description'] = self.collection_oauth.description
        info['comment'] = self.collection_oauth.comment_count

        self.info_list.append(info)
        self.info_url_complete_set.add(target_url)
        self.catch_content()
        return

    def catch_content(self):
        for item in self.collection_oauth.answers:
            answer = dict()
            question = dict()
            get_answer_dict(answer=answer, item=item)
            question['question_id'] = item.question.id
            question['title'] = item.question.title
            self.answer_list += [answer]
            self.question_list += [question]

        self.add_collection_index(self.info_list[0]['collection_id'], self.answer_list)

    def add_collection_index(self, collection_id, answer_list):
        for answer in answer_list:
            data = {
                'href': answer['href'],
                'collection_id': collection_id,
            }
            self.collection_index_list.append(data)
        return

    def create_save_config(self):
        config = {
            'Answer': self.answer_list,
            'Question': self.question_list,
            'CollectionInfo': self.info_list,
            'CollectionIndex': self.collection_index_list,
        }
        return config

    def create_work_set(self, target_url):
        pass

    def clear_index(self):
        collection_id_tuple = tuple(set(x['collection_id'] for x in self.collection_index_list))
        sql = 'DELETE from CollectionIndex where collection_id in ({})'.format((' ?,' * len(collection_id_tuple))[:-1])
        DB.cursor.execute(sql, collection_id_tuple)
        DB.commit()
        return


class TopicWorker(PageWorker):
    topic_index_list = []
    topic_id = None
    topic_oauth = None

    def create_work_set(self, target_url):
        pass

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        _client_load_token()
        self.topic_id = Match.topic(target_url).group('topic_id')
        self.topic_oauth = client.topic(int(self.topic_id))

        info = dict()

        info['title'] = self.topic_oauth.name
        info['topic_id'] = self.topic_oauth.id
        info['logo'] = self.topic_oauth.avatar_url
        info['follower'] = self.topic_oauth.follower_count
        info['description'] = self.topic_oauth.introduction

        self.info_list.append(info)
        self.info_url_complete_set.add(target_url)
        self.catch_content()
        return

    def catch_content(self):
        for item in self.topic_oauth.best_answers:
            answer = dict()
            question = dict()
            get_answer_dict(answer=answer, item=item)
            question['question_id'] = item.question.id
            question['title'] = item.question.title
            self.answer_list += [answer]
            self.question_list += [question]

        self.add_topic_index(self.info_list[0]['topic_id'], self.answer_list)

    def add_topic_index(self, topic_id, answer_list):
        for answer in answer_list:
            data = {
                'href': answer['href'],
                'topic_id': topic_id,
            }
            self.topic_index_list.append(data)
        return

    def create_save_config(self):
        config = {
            'Answer': self.answer_list,
            'Question': self.question_list,
            'TopicInfo': self.info_list,
            'TopicIndex': self.topic_index_list,
        }
        return config

    def clear_index(self):
        topic_id_tuple = tuple(set(x['topic_id'] for x in self.topic_index_list))
        sql = 'DELETE from TopicIndex where topic_id in ({})'.format((' ?,' * len(topic_id_tuple))[:-1])
        DB.cursor.execute(sql, topic_id_tuple)
        DB.commit()
        return


class ColumnWorker(PageWorker):
    u"""
    专栏没有Parser, 因为有api
    """
    column_id = None

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        result = Match.column(target_url)
        self.column_id = result.group('column_id')
        content = Http.get_content('https://zhuanlan.zhihu.com/api/columns/' + self.column_id)
        if not content:
            return
        raw_info = json.loads(content)
        info = dict()
        info['creator_id'] = raw_info['creator']['slug']
        info['creator_hash'] = raw_info['creator']['hash']
        info['creator_sign'] = raw_info['creator']['bio']
        info['creator_name'] = raw_info['creator']['name']
        info['creator_logo'] = raw_info['creator']['avatar']['template'].replace('{id}', raw_info['creator']['avatar'][
            'id']).replace('_{size}', '')

        info['column_id'] = raw_info['slug']
        info['name'] = raw_info['name']
        info['logo'] = raw_info['creator']['avatar']['template'].replace('{id}', raw_info['avatar']['id']).replace(
            '_{size}', '')
        info['article'] = raw_info['postsCount']
        info['follower'] = raw_info['followersCount']
        info['description'] = raw_info['description']
        self.info_list.append(info)
        self.task_complete_set.add(target_url)
        detect_url = 'https://zhuanlan.zhihu.com/api/columns/{}/posts?limit=10&offset='.format(self.column_id)
        for i in range(info['article'] / 10 + 1):
            self.work_set.add(detect_url + str(i * 10))
        return

    def parse_content(self, content):
        article_list = json.loads(content)
        for info in article_list:
            article = dict()
            article['author_id'] = info['author']['slug']
            article['author_hash'] = info['author']['hash']
            article['author_sign'] = info['author']['bio']
            article['author_name'] = info['author']['name']
            article['author_logo'] = info['author']['avatar']['template'].replace('{id}', info['author']['avatar'][
                'id']).replace('_{size}', '')

            article['column_id'] = self.column_id
            article['name'] = info['title']
            article['article_id'] = info['slug']
            url = info['url']
            article['href'] = u'https://zhuanlan.zhihu.com' + url
            article['title'] = info['title']
            article['title_image'] = info['titleImage']
            article['content'] = info['content']
            article['comment'] = info['commentsCount']
            article['agree'] = info['likesCount']
            article['publish_date'] = info['publishedTime'][:10]
            self.answer_list.append(article)
        return

    def create_save_config(self):
        config = {
            'ColumnInfo': self.info_list,
            'Article': self.answer_list
        }
        return config
