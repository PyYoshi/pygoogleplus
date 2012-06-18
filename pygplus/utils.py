# -*- coding:utf-8 -*-

# TODO: すべてxpathに置き換えて、lxmlがimport可能であればそれを使い、ダメな場合BeautifulSoupを使うようにする。 これである程度高速化を図れる。
# TODO: BeautifulSoup4への移行

import random
import re
from datetime import datetime
import time

from pygplus.errors import PyGplusErrors

from bs4 import BeautifulSoup

__all__ = ['Utils']

preFixJsonHead = re.compile(r'^\)\]\}\'(.*)')
preFixJsonBracket = re.compile(r'\[\,')
preFixJsonDoubleComma = re.compile(r'\,\,')
preFixJsonIntAfterBracket = re.compile(r'\,\{(\d+)\:')
preExtractInitData=re.compile(r'AF_initDataCallback\(\{key\:\s\'(.*)\'\,\sisError\:\s\s(.*)\s\,\sdata\:\s(.*)\}\)\;')

class Utils(object):
    @staticmethod
    def gen_reqid(max_digits=7):
        """
        POST時に必要な"_reqid"を生成
        Generate 7digits number.
        Args:
            none
        Returns:
            reqid: Integer
                7桁のランダム数値
        Exceptions:
            none
        """
        if max_digits > 7:
            raise PyGplusErrors(u'max_digitsは7以上は不正です。')
        elif max_digits < 1:
            raise PyGplusErrors(u'max_digitsは1未満は不正です。')
        min = 1000000
        max = 9999999
        reqid = str(random.uniform(min,max)).split('.')[0]
        return reqid[:max_digits]

    @staticmethod
    def build_path(host,path,ssl=False):
        if ssl:
            return 'https://'+ host + path
        else:
            return 'http://'+ host + path

    @staticmethod
    def import_simplejson():
        try:
            import simplejson as json
        except ImportError:
            try:
                import json
            except ImportError:
                try:
                    from django.utils import simplejson as json
                except ImportError:
                    raise ImportError, "Can't load a json library"
        return json

    @staticmethod
    def fix_json_string(str):
        line = ''
        for s in str.splitlines():
            line += s
        m = preFixJsonHead.match(line)
        if m:
            line = m.group(1)
        line = re.sub(preFixJsonBracket,'[null,',line)
        while True:
            m = preFixJsonDoubleComma.search(line)
            if m:
                line = re.sub(preFixJsonDoubleComma,',null,',line)
            else:
                break
        while True:
            m = preFixJsonIntAfterBracket.search(line)
            if m:
                line = re.sub(preFixJsonIntAfterBracket,',{"'+m.group(1)+'":',line)
            else:
                break
        return line

    @staticmethod
    def extract_initdata_json_string_list(str):
        soup = BeautifulSoup(str,from_encoding="utf-8")
        scripts = []
        for script in soup.findAll('script'):
            line = ''
            for s in script.text.splitlines():
                line += s
            m = preExtractInitData.match(line)
            if m:
                key = m.group(1)
                isError = m.group(2)
                script = Utils.fix_json_string(m.group(3))
                scripts.append({
                    'key':key,
                    'isError':isError,
                    'data':script
                })
        return scripts

    @staticmethod
    def conv_jsdate2datetime(unixtime_str):
        unixtime = int(unixtime_str)/1000
        return datetime.fromtimestamp(unixtime)

    @staticmethod
    def get_jsdate_now():
        return str(int(time.mktime(datetime.now().timetuple())*1000))

    @staticmethod
    def parse_divclassvu(str):
        soup = BeautifulSoup(str)
        div = soup.find('div',{'class':'vu'})
        line = ''
        for s in div.text.splitlines():
            line += s
        return Utils.fix_json_string(line.replace('&quot;','"'))
