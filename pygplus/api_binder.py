# -*- coding:utf-8 -*-

import urllib2
import gzip
import cStringIO

from pygplus.errors import PyGplusErrors
from pygplus.utils import Utils
from pygplus.parser import ModelParser

class ApiBinder(object):
    """ 通信関係の処理 """
    def __init__(self,**config):
        """

        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """

        # 初期値
        self.headers = [
            ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5'),
            ("Accept-encoding", "gzip"), # 高速化
        ]

        self.api = config.get('api',None)
        self.api_method_path = config.get('api_method_path',None)
        self.referer = config.get('referer',None)
        self.required_auth = config.get('required_auth',False)
        self.method_post = config.get('method_post',False)
        self.post_body = config.get('post_body',None)

        if self.referer:
            self.headers.append(
                ('Referer', self.referer)
            )

    def execute(self,model):
        """
        description
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        # TODO: 例外処理を追加 # raise PyGplusErrors('HttpCommunicationError: mes',res)
        url = Utils.build_path(self.api.host,self.api_method_path,self.api.ssl)
        if self.required_auth:
            if not self.api.auth:
                raise PyGplusErrors('Required auth_handler.')
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.api.auth.cookie))
        else:
            self.opener = urllib2.build_opener()
        self.opener.addheaders = self.headers
        if self.method_post:
            res = self.opener.open(url,data=self.post_body)
        else:
            res = self.opener.open(url)

        data = res.read()
        if res.headers.get('content-encoding', None) == 'gzip':
            data = gzip.GzipFile(fileobj=cStringIO.StringIO(data)).read()

        parser = ModelParser()
        return parser.parser(self,model,data)



  