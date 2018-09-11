# -*- coding: utf-8 -*-

"""
Python Uitils Library
~~~~~~~~~~~~~~~~~~~~~

Get demand time from all kinds of original time format after delay without specified type.
输入各类格式时间，输出延迟后的指定格式时间，无需指定时间类型。

Usage:

   >>> from zzzutils import *
   >>> get_time('20180911')
   '2018-09-11 00:00:00'
   >>> get_time('20180911', fmt=0)
   1536595200
   >>> get_time(1536595200)
   '2018-09-11 00:00:00'
   >>> get_time('2018-09-11 16:23:19', fmt=8)
   '20180911'
   >>> get_time('2018-09-11 16:23:19', delay=-3600)
   '2018-09-11 15:23:19'

Args: [original_time] [delay] [output_fmt:{0,6,8,10,16,17,19}]
Input format(Any one of them): 
#   201809
#   20180910
#   2018-09-10
#   2018-09-10 18:00
#   20180910-18:00:00
#   2018-09-10 18:00:00
#   1536573600(int)
#   1536573600.00(float)
Return format(Any one of them): 
#   201809
#   20180910
#   2018-09-10
#   2018-09-10 18:00
#   20180910-18:00:00
#   2018-09-10 18:00:00
#   1536573600(int)

:license: Apache 2.0, see LICENSE for more details.
"""

name = "zzzutils"
from zzzutils import *