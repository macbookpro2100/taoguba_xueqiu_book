#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ..html5lib.constants import entities

html5_entities = {k.replace(';', ''): v for k, v in entities.iteritems()}

# print html5_entities