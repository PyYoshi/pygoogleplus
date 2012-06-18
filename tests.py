# coding:utf8

# nosetests --with-profile --profile-stats-file nose.prof tests.py
# python -c "import hotshot.stats ; stats = hotshot.stats.load('nose.prof') ; stats.sort_stats('time', 'calls') ; stats.print_stats(20)"
# hotshot2dot nose.prof| dot -Tpng -o profile.png


from pygplus.auth_handler import AuthHandler
from pygplus.api_handler import ApiHandler
from pygplus.builder import Builder

import settings

# Conf
email = settings.EMAIL
passwd = settings.PASSWD
other_user_id = "109813896768294978296" # Sergey Brin
photo_filename = r""


class Tests():
    def __init__(self):
        self.api = ApiHandler(auth_handler=AuthHandler(email=email,passwd=passwd))

    def test_getuserinfo1(self):
        self.api.get_user_info(other_user_id)
