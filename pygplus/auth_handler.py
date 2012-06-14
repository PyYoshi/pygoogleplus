# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib

from BeautifulSoup import BeautifulSoup

from pygplus.errors import PyGplusErrors

__all__ = ['AuthHandler']

class AuthHandler(object):
    def __init__(self,email=None,passwd=None,cookie=None):
        """
        description
        Args:
            email:
            passwd:
        Returns:
            none
        Exceptions:
            none
        """
        # TODO: pickleもしくはemailとpasswdが入力されていないとエラーが出るようになっているが、他の手法でcookieを受け付ける手段を作る
        # TODO: cookieの場合、ログインが正常に行えるものなのかチェックする必要がある。 expiresからのチェック？
        if not email and not cookie:
            raise PyGplusErrors(u"emailとpasswd、もしくはcookie_pickleが入力されていません。")
        if cookie:
            self.cookie = cookie
        else:
            self.cookie = self.__get_cookie(email,passwd)

    def __get_cookie(self,email,passwd):
        """
        description
        Args:
            email:
            passwd:
        Returns:
            content: cookie string
        Exceptions:
            PyGplusErrors
        """
        try:
            url = 'https://accounts.google.com/ServiceLoginAuth'
            cjar = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cjar))
            headers = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.942.0 Safari/535.8')]
            opener.addheaders = headers
            content = opener.open(url)
            soup = BeautifulSoup(content)
            dsh = soup.find('input',{'name':'dsh'}).get('value')
            galx = soup.find('input',{'name':'GALX'}).get('value')
            body = {'Email': email,
                    'Passwd': passwd,
                    'GALX': galx,
                    'dsh': dsh,
                    'continue': 'https://plus.google.com/',
                    'dnConn': 'https://accounts.youtube.com',
                    'PersistentCookie':'yes',
                    'ltmpl':'	gposl920',
                    'pstMsg':1,
                    'rmShown':1,
                    'secTok': '',
                    'timeStmp': '',
                    'signIn': "Sign in",
            }
            res = opener.open(url,urllib.urlencode(body))
            if res.code == 200:
                return cjar
            else:
                raise PyGplusErrors("Google Login Error.",res)
        except Exception,e:
            raise PyGplusErrors(e)

    def save_cookie(self,filename):
        self.cookie.save(filename=filename)

