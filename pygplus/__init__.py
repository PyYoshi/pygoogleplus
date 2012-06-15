# -*- coding:utf-8 -*-
__author__ = 'PyYoshi'
__license__ = 'MIT'
__version__ = '1.1.0' # X.Y.Z: X is major version. Y is minor version. Z is revision.
__url__ = 'https://github.com/PyYoshi/pygoogleplus'
# Histroy
# 1.0.0: メジャーアップデート
# 1.0.1: ApiHandler.self_infoが無い場合、強制的に取得するように変更
#        細かな修正
# 1.1.0: 投稿できないバグの修正。
#        Apiの使用方法の変更によるマイナーバージョンのアップデート
#        ApiHandler.__get_self_info()の追加。 所有しているPagesの修得が可能になりました。

from pygplus.api_handler import ApiHandler
from pygplus.auth_handler import AuthHandler
from pygplus.errors import PyGplusErrors
from pygplus.builder import Builder