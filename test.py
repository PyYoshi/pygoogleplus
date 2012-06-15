# -*- coding:utf-8 -*-
__AUTHOR__ = 'RenaX'
__LICENCE__ = ''
__VERSION__ = ''

import settings

from pygplus.auth_handler import AuthHandler
from pygplus.api_handler import ApiHandler
from pygplus.builder import Builder
import cookielib

# cookieをファイルへ保存
#auth = AuthHandler(email=settings.EMAIL,passwd=settings.PASSWD)
#auth.save_cookie(settings.CJAR_PATH)

# ファイルに保存したcookieからapiを叩く
cookie = cookielib.LWPCookieJar()
cookie.load(settings.CJAR_PATH)
auth = AuthHandler(cookie=cookie)
#print auth.cookie._cookies[".google.com"]["/"]["APISID"].value
api = ApiHandler(auth_handler=auth)

print api.get_user_info().__dict__
##prof = api.get_user_info()
##print prof.__dict__
##print prof.posts[5].__dict__
##print prof.posts[5].comments[0].__dict__
##next_id = prof.next_id
##next_obj = prof.next_obj
##print next_obj
##print '================================================================'
##print api.get_user_info(next_id=next_id,next_obj=next_obj).posts
##print api.get_user_info(user_id='102878059071970571610').__dict__
##print api.get_post_info(item_id='z12gcjqxeknmjfa2l22nfhzagqq4sntvi').posts[0].__dict__
##print api.get_followers().__dict__
##print api.get_circles().__dict__
##print api.update_post(message=u'Public _test_ @115589978196270409444',scope_type=Builder.ANYONE)
##print api.update_post(message=u'CIRCLES _test_  @115589978196270409444',scope_type=Builder.CIRCLES)
##print api.update_post(message=u'EXTENDED _test_ @115589978196270409444',scope_type=Builder.EXTENDED)
##print api.update_post(message=u'LIMITED _test_ @115589978196270409444',scope_type=Builder.LIMITED,circle_ids=['5b9a8fd30a6e6e3a'])
##print api.update_post(message=u'LIMITED Reply _test_ @104560124403688998123',scope_type=Builder.LIMITED,circle_ids=['5b9a8fd30a6e6e3a'])
##print api.update_comment(u'Ahhhhhhhhhhhhhhhhhhhh',item_id='z12gupjhuviwyxdyr04cipnhfwuec50gz4c') # TODO: とどいたかわからん
##media = api.media_photo(filenames=[r'F:\ce1a8ee8ff83dbaff6298a91fd5986a01b8e32a1.gif'])
##print api.update_post(message=u'画像投稿テスト',scope_type=Builder.ANYONE,media=media).__dict__
##media=api.media_link('http://www.nicovideo.jp/video_top')
##print api.update_post(message=u'リンクテスト',scope_type=Builder.ANYONE,media=media).__dict__
##media=api.media_video('http://www.youtube.com/watch?v=KQ6zr6kCPj8')
##print api.update_post(message=u'ようつべリンクテスト',scope_type=Builder.ANYONE,media=media).__dict__
##print api.get_notification().__dict__
##print api.get_dashboard().__dict__
##print '================================================================'
##dashboard = api.get_dashboard()
##print dashboard.posts
##next_id = dashboard.next_id
##next_obj = dashboard.next_obj
##print next_obj
##print '================================================================'
##print api.get_dashboard(next_id=next_id,next_obj=next_obj).posts
##item_id = 'z13vx5nyeravynsit04cipnhfwuec50gz4c'
##print api.update_post_plusone(item_id=item_id)
##print api.update_post_unplusone(item_id=item_id)
##item_id = 'z13zwxerisfuxfmrc04cipnhfwuec50gz4c'
##print api.delete_post(item_id=item_id)

##print api.update_post(message='コメント削除テスト',scope_type=Builder.ANYONE)
##item_id = 'z12nyjhymknfifzod04cipnhfwuec50gz4c'
#print api.update_comment(message='あ',item_id=item_id).__dict__
##comment_id = 'z123j1ly4s2yzzgh304cipnhfwuec50gz4c#1337691980870545'
##print api.delete_comment(comment_id=comment_id)

##print api.update_disable_comment(item_id)
##print api.update_enable_comment(item_id)
##print api.update_lock_post(item_id)
##print api.update_unlock_post(item_id)

##print api.lookup_hovercards('115676515375527554873').__dict__

