#!/usr/bin/env python
# -*- coding: utf-8 -*-
__appname__ = 'EE-Book'

import os
import sys

# 为了能够从上一级目录中导入constants模块
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
