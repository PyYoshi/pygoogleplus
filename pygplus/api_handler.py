# -*- coding:utf-8 -*-

import urllib
import os

from pygplus.errors import PyGplusErrors
from pygplus.api_binder import ApiBinder
from pygplus.utils import Utils
from pygplus.builder import Builder

# TODO: self_infoのatやcircle情報が欲しくて直接APIを叩く場合があるが、それは不適切な処理なのでExceptionするか、Developperに入力してもらうか、の形をとる必要がある。
# TODO: 各API関数のdocstringを書く
# TODO: atがなくてもうごくっぽい。 要調査

class ApiHandler(object):
    def __init__(self,auth_handler,at=None,retry_times=0,retry_delay=0):
        self.auth = auth_handler
        self.retry_times = retry_times
        self.retry_delay = retry_delay
        self.host = "plus.google.com"
        self.ssl = True
        self.self_info = None
        self.at = at
        self.followers = None
        self.followings = None
        self.own_circles = None

    def template(self):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        raise NotImplementedError()
        api_method_path = "/"
        required_auth = True
        method_post = False
        model = ""
        binder = ApiBinder(self)
        binder.execute(model)
        return

    def get_user_info(self,user_id=None,next_id=None,next_obj=None,forced=False):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        # https://plus.google.com/u/0/_/pages/getidentities/?hl=ja&_reqid=167621&rt=j # 自分の場合はこれでいい
        if next_id and next_obj: # TODO: あほ処理
            forced = True
        if user_id == None:
            if self.self_info != None and forced == False:
                return self.self_info
            else:
                api_method_path = "/me/about"
        else:
            api_method_path = "/%s/about" % str(user_id)
        required_auth = True
        method_post = False
        model = "userinfo"
        if next_id:
            result = self.__get_nextdata(next_id=next_id,next_obj=next_obj)
        else:
            binder = ApiBinder(api=self,
                               api_method_path=api_method_path,
                               required_auth=required_auth,
                               method_post=method_post
            )
            result = binder.execute(model)
            self.self_info = result

        return result

    def __get_nextdata(self,next_id,next_obj):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'nextpostsdata'
        api_method_path = "/_/stream/getactivities/?"
        params = {
            '_reqid' : Utils.gen_reqid(max_digits=6),
            'rt':'j'
        }
        api_method_path += urllib.urlencode(params)
        at = self.self_info.at # TODO: 問題の処理
        f_req = Builder.build_nextdata_json(next_id=next_id,next_obj=next_obj)
        post_body = urllib.urlencode({
            'at':at,
            'f.req': f_req
        })
        required_auth = True
        method_post = True
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def get_post_info(self,item_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        api_method_path = "/_/stream/getactivity/?"
        params = {
            '_reqid': Utils.gen_reqid(),
            'rt':'j',
            'updateId':item_id
        }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = False
        model = "jsonraw"
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post
        )
        result = binder.execute(model)
        return result

    def get_notification(self,max_results=50):
        """
        Description...
        Args:
            none
        Retruns:
            none
        Exceptions:
            none
        """
        # https://plus.google.com/u/0/_/notifications/getnotificationsdata?maxResults=15&hl=ja&_reqid=65366&rt=j
        api_method_path = "/_/notifications/getnotificationsdata?"
        params = {
            #'inWidget':'true',
            #'fetchUnreadCount':'true',
            'maxResults':max_results, # 最大50 バグる可能性があるので
            '_reqid':Utils.gen_reqid(),
            'rt':'j'
        }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = False
        model = "jsonraw"
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post
        )
        result = binder.execute(model)
        return result

    def get_followers(self,page_id=None,forced=False):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        if self.followers != None and forced == False:
            return self.followers
        api_method_path = "/_/socialgraph/lookup/followers/?"
        required_auth = True
        method_post = False
        model = 'followers'
        params = {
            "m":10000,
            "_reqid":Utils.gen_reqid(),
            "rt":"j"
        }
        api_method_path += urllib.urlencode(params)
        binder = ApiBinder(api=self,
                           api_method_path=api_method_path,
                           required_auth=required_auth,
                           method_post=method_post
        )
        result = binder.execute(model)
        self.followers = result.users
        return result

    def get_circles(self,page_id=None,forced = False):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        if self.own_circles != None and forced == False:
            return self.own_circles
        api_method_path = "/_/socialgraph/lookup/circles/?"
        params = {
            'ct':2,
            'm':True,
            'tag':'fg',
            "_reqid":Utils.gen_reqid(),
            'rt':'j',
        }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = False
        model = 'circles'
        binder = ApiBinder(api=self,
                           api_method_path=api_method_path,
                           required_auth=required_auth,
                           method_post=method_post
        )
        result = binder.execute(model)
        self.followings = result.following_users
        self.own_circles = result.circles_list
        return result

    def get_dashboard(self,next_id=None,next_obj=None):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        api_method_path = "/"
        required_auth = True
        method_post = False
        model = "dashboard"

        if not self.self_info:
            raise PyGplusErrors(u'apt.get_user_info()が実行されていません。')
        if next_id:
            result = self.__get_nextdata(next_id=next_id,next_obj=next_obj)
        else:
            binder = ApiBinder(api=self,
                api_method_path=api_method_path,
                required_auth=required_auth,
                method_post=method_post
            )
            result = binder.execute(model)
        return result

    def media_photo(self,filenames=[]):
        """
        Description...
        
        Args:
            none
        Returns:
            {
                'type':'photos',
                'result' : [{
                    '_api': <pygplus.api_handler.ApiHandler>,
                    'photo': {
                        'username': str,
                        'description': str,
                        'album_id': str,
                        'timestamp': datetime.datetime(),
                        'photo_page_url': str,
                        'height': int
                        'photo_url': str,
                        'mimetype': str,
                        'kind': str,
                        'photo_id': str,
                        'album_page_url': str,
                        'filename': str,
                        'width': int,
                        'auto_downsize': bool,
                        'size': int
                    }]
                }
            }
        Exceptions:
            none
        """
        api_method_path = "/_/upload/photos/resumable?"
        required_auth = True
        method_post = True
        params={
            "authuser":0
        }
        api_method_path += urllib.urlencode(params)
        model = 'uploadphoto'
        results = []
        for filename in filenames:
            try:
                null ,fext = os.path.splitext(filename)
                if fext in ['.jpg','.jpeg','.png','.gif','.webp']:
                    fsize = os.path.getsize(filename)
                    jsonstr = Builder.build_photo_json(filename,fsize)
                    binder_pre = ApiBinder(
                        api=self,
                        api_method_path=api_method_path,
                        required_auth=required_auth,
                        method_post=method_post,
                        post_body=jsonstr
                    )
                    result = binder_pre.execute(model)
                    upload_url = result.photo['url']
                    fp = open(filename,'rb')
                    data = fp.read()
                    fp.close()
                    binder_upload = ApiBinder(
                        api=self,
                        api_method_path=upload_url.replace('https://plus.google.com',''),
                        required_auth=required_auth,
                        method_post=method_post,
                        referer='https://plus.google.com/_/apps-static/_/js/home/b,s/rt=h/ver=N57_ty_kvkI.ja./sv=1/am=!Qj_OVqIfUA3KS8WjzgNwC8gVlkRq1bUDZdv_su4/d=1/',
                        post_body=data
                    )
                    result = binder_upload.execute(model)
                    results.append(result)
            except IOError,e:
                fp.close()
                raise PyGplusErrors(e)
        result = {
            'type':'photos',
            'result':results
        }
        return result

    def media_link(self,url):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        api_method_path = "/_/sharebox/linkpreview/?"
        required_auth = True
        method_post = True
        params={
            "c":url,
            "t":1,
            "slpf":0,
            "ml":1,
            "_reqid":Utils.gen_reqid(),
        }
        api_method_path += urllib.urlencode(params)
        model = 'uploadlink'
        if self.self_info == None:
            self.get_user_info()
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'susp':	False,
            'at':at
        })
        binder = ApiBinder(api=self,
                           api_method_path=api_method_path,
                           required_auth=required_auth,
                           method_post=method_post,
                           post_body=post_body
        )
        result = binder.execute(model)
        return result

    def media_video(self,url):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        api_method_path = "/_/sharebox/linkpreview/?"
        required_auth = True
        method_post = True
        params={
            "c":url,
            "t":1,
            "slpf":0,
            "ml":1,
            "_reqid":Utils.gen_reqid(),
        }
        api_method_path += urllib.urlencode(params)
        model = 'uploadvideolink'
        if self.self_info == None:
            self.get_user_info()
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'susp':	False,
            'at':at
        })
        binder = ApiBinder(api=self,
                           api_method_path=api_method_path,
                           required_auth=required_auth,
                           method_post=method_post,
                           post_body=post_body
        )
        result = binder.execute(model)
        return result

    def update_post(self,message,scope_type,circle_ids=[],media=None,page_id=None,share=False,comment=False):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        if page_id != None:
            api_method_path = "/b/"+page_id+'/_/sharebox/post/?'
        else:
            api_method_path = "/_/sharebox/post/?"
        params = {
            "_reqid":Utils.gen_reqid(6),
            "rt":"j",
            "spam":20
        }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        model = 'updatepost'
        if self.self_info == None:
            self.get_user_info()
        user_id = self.self_info.user_id
        scope_data = Builder.build_scope_data(self,scope_type,user_id,circle_ids)
        if media:
            media_json = Builder.build_media_json(media)
            if media['type'] == 'photos':
                album_id=media['result'][0].photo['album_id']
            else:
                album_id=None
            spar = Builder.build_post_json(message=message,user_id=user_id,scope_data=scope_data,album_id=album_id,media_json=media_json,share=share,comment=comment)
        else:
            spar = Builder.build_post_json(message=message,user_id=user_id,scope_data=scope_data,share=share,comment=comment)
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'spar':spar,
            'at':at
        })
        binder = ApiBinder(api=self,
                           api_method_path=api_method_path,
                           required_auth=required_auth,
                           method_post=method_post,
                           post_body=post_body)
        result = binder.execute(model)
        return result

    def update_comment(self,message,item_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        if self.self_info == None:
            self.get_user_info()
        api_method_path = "/_/stream/comment/?"
        params = {
            "_reqid":Utils.gen_reqid(),
            "rt":"j",
        }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        at = self.self_info.at # TODO: 問題の処理
        timestamp = Utils.get_jsdate_now()
        clientId = item_id+':'+timestamp
        post_body = urllib.urlencode({
            'at':at,
            'clientId':clientId, # os:item_id#unixtime
            'itemId':item_id,
            'text':message,
            'timestamp_msec': timestamp
        })
        model = 'updatecomment'
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def update_plusone(self,item_id):
        """
        Description...
        投稿の場合はitem_id、コメントの場合はcomment_idでできる。
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'jsonraw'
        api_method_path = "/_/plusone?"
        params = {
            "_reqid":Utils.gen_reqid(),
            "rt":"j",
        }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'itemId':'buzz:'+item_id,
            'set':True,
            'at':at
        })
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def update_unplusone(self,item_id):
        """
        Description...
        投稿の場合はitem_id、コメントの場合はcomment_idでできる。
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'jsonraw'
        api_method_path = "/_/plusone?"
        params = {
            "_reqid":Utils.gen_reqid(),
            "rt":"j",
            }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'itemId':'buzz:'+item_id,
            'set':False,
            'at':at
        })
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def delete_post(self,item_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'jsonraw'
        api_method_path = "/_/stream/deleteactivity/?"
        params = {
            "_reqid":Utils.gen_reqid(), # 7桁以外だと400
            "rt":"j",
        }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'itemId':item_id,
            'at':at,
        })
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def delete_comment(self,comment_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'jsonraw'
        api_method_path = "/_/stream/deletecomment/?"
        params = {
            "_reqid":Utils.gen_reqid(),
            "rt":"j",
        }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'commentId':comment_id,
            'at':at,
            })
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def update_disable_comment(self,item_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'jsonraw'
        api_method_path = "/_/stream/disablecomments/?"
        params = {
            "_reqid":Utils.gen_reqid(),
            "rt":"j",
            }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True

        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'itemId':item_id,
            'disable':True,
            'at':at
        })
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def update_enable_comment(self,item_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'jsonraw'
        api_method_path = "/_/stream/disablecomments/?"
        params = {
            "_reqid":Utils.gen_reqid(),
            "rt":"j",
            }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'itemId':item_id,
            'disable':False,
            'at':at
        })
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def update_lock_post(self,item_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'jsonraw'
        api_method_path = "/_/stream/disableshare/?"
        params = {
            "_reqid":Utils.gen_reqid(),
            "rt":"j",
            }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'itemId':item_id,
            'disable':True,
            'at':at
        })
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def update_unlock_post(self,item_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'jsonraw'
        api_method_path = "/_/stream/disableshare/?"
        params = {
            "_reqid":Utils.gen_reqid(),
            "rt":"j",
            }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'itemId':item_id,
            'disable':False,
            'at':at
        })
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result

    def lookup_hovercards(self,user_id):
        """
        Description...

        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = 'hovercards'
        api_method_path = "/_/socialgraph/lookup/hovercards/?"
        params = {
            "_reqid":Utils.gen_reqid(6),
            "rt":"j",
            "sp": True,
            "n":7,
            "m":[[[None,None,user_id]]]
            }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True

        at = self.self_info.at # TODO: 問題の処理
        post_body = urllib.urlencode({
            'at':at
        })
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post,
            post_body=post_body)
        result = binder.execute(model)
        return result















    def update_post_share(self,message,item_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        raise NotImplementedError()
        api_method_path = "/"
        required_auth = True
        method_post = False

        binder = ApiBinder(self)
        pass

    def follow(self,user_id,circle_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        https://plus.google.com/_/socialgraph/mutate/modifymemberships/?_reqid=2622962&rt=j
        a	[[["61f2d65e88ffdbed"]]]
        at	AObGSAgVHPnpUIX2qM2xgaVaOehCshC33Q:1322471347000
        m	[[[[null,null,"116838657085891571936"],"Reina Akatsuki",[]]]]
        r	[[]]
        """
        raise NotImplementedError()
        api_method_path = "/"
        required_auth = True
        method_post = False
        model = ""
        binder = ApiBinder(self)
        binder.execute(model)
        return

    def unfollow(self,user_id,circle_id):
        """
        Description...
        Args:
            none
        Returns:
            none
        Exceptions:
            none

        https://plus.google.com/_/socialgraph/mutate/removemember/?_reqid=2422962&rt=j
        at	AObGSAgVHPnpUIX2qM2xgaVaOehCshC33Q:1322471347000
        c	["61f2d65e88ffdbed"]
        m	[[[null,null,"116838657085891571936"]]]
        """
        raise NotImplementedError()
        api_method_path = "/"
        required_auth = True
        method_post = False
        model = ""
        binder = ApiBinder(self)
        binder.execute(model)
        return



    