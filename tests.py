# coding:utf8

import unittest

from pygplus.auth_handler import AuthHandler
from pygplus.api_handler import ApiHandler
from pygplus.builder import Builder

# Conf
email = ""
passwd = ""
other_user_id = "109813896768294978296" # Sergey Brin
photo_filename = r""


class PyGplusAPITests(unittest.TestCase):
    def setUp(self):
        self.api = ApiHandler(auth_handler=AuthHandler(email=email,passwd=passwd))

    def test1_getuserinfo1(self):
        self.api.get_user_info()

    def test2_getuserinfo2(self):
        self.api.get_user_info()
        next_id = self.api.self_info.next_id
        next_obj = self.api.self_info.next_obj
        self.api.get_user_info(next_id=next_id,next_obj=next_obj)

    def test3_getuserinfo3(self):
        self.api.get_user_info(user_id=other_user_id)

    def test4_getpostinfo(self):
        self.api.self_info.posts[0][]
