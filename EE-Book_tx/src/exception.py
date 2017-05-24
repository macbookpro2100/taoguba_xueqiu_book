#!/usr/bin/env python2
# -*- coding: utf-8 -*-


__all__ = [
    "UnexpectedResponseException",
    "NeedCaptchaException",
    "NeedLoginException"
]


class UnsupportTypeException(BaseException):
    def __init__(self, what):
        self.what = what

    def __str__(self):
        return '{self.what}\nUnsupported type.'.format(self=self)
