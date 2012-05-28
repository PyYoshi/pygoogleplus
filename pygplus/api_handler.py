# -*- coding:utf-8 -*-

import urllib
import os

from pygplus.errors import PyGplusErrors
from pygplus.api_binder import ApiBinder
from pygplus.utils import Utils
from pygplus.builder import Builder

# TODO: 各API関数のdocstringを書く
# TODO: atがなくてもうごくっぽい。 要調査

class ApiHandler(object):
    """ 叩けるAPIの関数群 """
    def __init__(self,auth_handler,self_info=None,user_id=None,at=None,retry_times=0,retry_delay=0):
        """
        APIHandlerのコンストラクタ
        Args:
            auth_handler: AuthHandler, Google+にログインする際に必要な引数。
            self_info: UserInfo(Model), 各APIを扱う際に必要な情報をまとめて入れることができます。 ApiHandler.get_user_info()の返り値を代入してください。 それ以外ではエラーを吐きます。
            user_id: str, ApiHandler.get_user_info()を実行するコストが気に入らない場合は、ここに自分のuser_idを代入してください。 またuser_idを入れた場合、at引数にも代入してください。
            at: str, ApiHandler.get_user_info()を実行するコストが気に入らない場合は、ここに自分のatを代入してください。 またatを入れた場合、user_id引数にも代入してください。
            retry_times: int, APIの実行に失敗した際に試行する回数。
            retry_delay: int, APIの実行に失敗した際に試行する際のラグ。
        Returns:
            none
        Exceptions:
            none
        """
        self.auth = auth_handler
        self.retry_times = retry_times
        self.retry_delay = retry_delay
        self.host = "plus.google.com"
        self.ssl = True
        self.self_info = self_info
        self.user_id = user_id
        self.at = at
        self.followers = None
        self.followings = None
        self.own_circles = None

    def template(self):
        """
        テンプレ。
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
        ユーザ情報を取得します。user_idを指定しない場合は自分の情報を取得します。
        Args:
            user_id: str, 得たいユーザのidを代入してください。
            next_id: str,, １度目には取得しきれなかった投稿を取得する際に必要となる値です。この関数の２回目以降の実行時にのみ使用できます。 返り値に格納されています。
            next_obj: obj, １度目には取得しきれなかった投稿を取得する際に必要となる値です。この関数の２回目以降の実行時にのみ使用できます。 返り値に格納されています。
            forced: bool, 強制的に取得する際はTrueにしてください。 デフォルトでは１度取得したものが返り値となります。
        Returns:
            UserInfo(Model)
        Exceptions:
            none
        """
        # https://plus.google.com/u/0/_/pages/getidentities/?hl=ja&_reqid=167621&rt=j # 自分の場合はこれでいい
        if next_id and next_obj:
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
            if not next_obj:
                raise PyGplusErrors('next_objがありません。')
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
        次のデータを取得する際に必要となる関数
        Args:
            next_id: str,, １度目には取得しきれなかった投稿を取得する際に必要となる値です。この関数の２回目以降の実行時にのみ使用できます。 返り値に格納されています。
            next_obj: obj, １度目には取得しきれなかった投稿を取得する際に必要となる値です。この関数の２回目以降の実行時にのみ使用できます。 返り値に格納されています。
        Returns:
            NextPostsData(Model)
        Exceptions:
            PyGplusErrors
        """
        model = 'nextpostsdata'
        api_method_path = "/_/stream/getactivities/?"
        params = {
            '_reqid' : Utils.gen_reqid(max_digits=6),
            'rt':'j'
        }
        api_method_path += urllib.urlencode(params)
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        指定されたidから投稿の情報を取得します
        Args:
            item_id: Posts(Model)の各投稿に格納されているitem_id。
        Returns:
            PostInfo(Model)
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
        model = "postinfo"
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post
        )
        result = binder.execute(model)
        return result

    def get_notification(self,max_results=50):
        """
        通知情報の取得。詳細情報はApiHandler.get_post_info()を実行してください。
        Args:
            max_results: int, 取得する通知の最大数。 50超は非推奨
        Retruns:
            Notifications(Model)
        Exceptions:
            none
        """
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
        model = "notifications"
        binder = ApiBinder(api=self,
            api_method_path=api_method_path,
            required_auth=required_auth,
            method_post=method_post
        )
        result = binder.execute(model)
        return result

    def get_followers(self,forced=False):
        """
        フォロワー情報の取得
        Args:
            forced: bool, 強制更新するか否か
        Returns:
            Followers(Model)
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

    def get_circles(self,forced=False):
        """
        サークル情報・フォローしているユーザ情報の取得
        Args:
            forced: bool, 強制更新するか否か
        Returns:
            Circles(Model)
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

    def get_dashboard(self,circle_id=None,next_id=None,next_obj=None):
        """
        ダッシュボード(ストリーム)から投稿情報を取得
        # TODO: わかりにくい関数名かもしれない。
        Args:
            circle_id: str, 取得したいcircle_id。ない場合はホームから取得する。
            next_id: str, １度目には取得しきれなかった投稿を取得する際に必要となる値です。この関数の２回目以降の実行時にのみ使用できます。 返り値に格納されています。
            next_obj: obj, １度目には取得しきれなかった投稿を取得する際に必要となる値です。この関数の２回目以降の実行時にのみ使用できます。 返り値に格納されています。
        Returns:
            Dashboard(Model)
        Exceptions:
            PyGplusErrors
        """
        api_method_path = "/"
        required_auth = True
        method_post = False
        model = "dashboard"

        if next_id:
            if not next_obj:
                raise PyGplusErrors('next_objがありません。')
            if circle_id:
                next_obj[3] = circle_id
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
        投稿に画像を含める際に使用する関数
        Args:
            filenames: list, アップロードしたいfileパスをリスト形式で代入してください。
        Returns:
            {
                'type':'photos',
                'result':results
            }
            results: list, UploadPhoto(Model)で構成されたリスト。
        Exceptions:
            PyGplusErrors
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
        投稿にリンクを含める際に使用する関数
        Args:
            url: str, リンク
        Returns:
            UploadLink(Model)
        Exceptions:
            PyGplusErrors
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        投稿にYoutubeリンクを含める際に使用する関数
        動画自体のアップロードは対応予定なし
        Args:
            url: str, youtubeのリンク
        Returns:
            UploadVideoLink
        Exceptions:
            PyGplusErrors
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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

    def update_post(self,message,scope_type,circle_ids=[],media=None,share=False,comment=False):
        """
        投稿するための関数
        Args:
            message: str, 投稿本文
            scope_type: Builder.ANYONE: 一般公開
                        Builder.EXTENDED: 友だちの友だちサークル公開
                        Builder.CIRCLES: あなたのサークル
                        Builder.LIMITED: サークル指定。 これを指定した場合、circle_idsは必須です。
            media: obj, ApiHandler.media_photo ApiHandler.media_link ApiHandler.media_videoのいずれかの返り値を代入してください。
            share: bool, Trueの場合、投稿ロック(共有無効)にします。
            comment: bool, Trueの場合、コメントを無効にします。
        Returns:
            UpdatePost(Model)
        Exceptions:
            PyGplusErrors
        """
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
        if self.self_info or self.user_id:
            user_id = self.self_info.user_id or self.user_id
        else:
            raise PyGplusErrors('user_idがありません。get_user_info()を実行するかAPIHandlerにuser_idを引数に入れてください。')
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        投稿にコメントする関数
        Args:
            message: str, コメント本文
            item_id: str, コメントしたい投稿のitem_id
        Returns:
            UpdateComment(Model)
        Exceptions:
            PyGplusErrors
        """
        api_method_path = "/_/stream/comment/?"
        params = {
            "_reqid":Utils.gen_reqid(),
            "rt":"j",
        }
        api_method_path += urllib.urlencode(params)
        required_auth = True
        method_post = True
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        投稿に+1する関数
        投稿の場合はitem_id、コメントの場合はcomment_idでできる。
        Args:
            item_id: str, +1したい投稿のitem_id
        Returns:
            JsonRaw(Model): 特に必要とする情報が含まれていないため、そのまま値を返す。
        Exceptions:
            PyGplusErrors
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        +1された投稿を取り消す関数
        投稿の場合はitem_id、コメントの場合はcomment_idでできる。
        Args:
            item_id: str, 取り消したい投稿のitem_id
        Returns:
            JsonRaw(Model): 特に必要とする情報が含まれていないため、そのまま値を返す。
        Exceptions:
            PyGplusErrors
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        投稿を削除する関数
        Args:
            item_id: str, 削除したい投稿のitem_id
        Returns:
            JsonRaw(Model): 特に必要とする情報が含まれていないため、そのまま値を返す。
        Exceptions:
            PyGplusErrors
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        コメントを削除する
        自分の投稿へのコメントの場合、自分のコメントでも削除できてしまうので注意が必要
        Args:
            comment_id: str, 削除したい投稿のcomment_id
        Returns:
            JsonRaw(Model): 特に必要とする情報が含まれていないため、そのまま値を返す。
        Exceptions:
            PyGplusErrors
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        投稿へのコメントを無効にする関数
        Args:
            item_id, str, 無効にしたい投稿のitem_id
        Returns:
            JsonRaw(Model): 特に必要とする情報が含まれていないため、そのまま値を返す。
        Exceptions:
            PyGplusErrors
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

        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        投稿へのコメントを有効にする関数
        Args:
            item_id: str, コメントを有効にしたい投稿のitem_id
        Returns:
            JsonRaw(Model): 特に必要とする情報が含まれていないため、そのまま値を返す。
        Exceptions:
            PyGplusErrors
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        投稿をロックし共有を無効化する関数
        Args:
            item_id: str, ロックしたい投稿のitem_id
        Returns:
            JsonRaw(Model): 特に必要とする情報が含まれていないため、そのまま値を返す。
        Exceptions:
            PyGplusErrors
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        共有無効化をアン・ロックする関数
        Args:
            item_id: str, ロック解除したい投稿のitem_id
        Returns:
            JsonRaw(Model): 特に必要とする情報が含まれていないため、そのまま値を返す。
        Exceptions:
            PyGplusErrors
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
        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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
        ユーザの簡易情報取得関数
        Args:
            user_id: str, 簡易情報を得たいユーザのuser_id
        Returns:
            HoverCards(Model)
        Exceptions:
            PyGplusErrors
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

        if self.self_info or self.at:
            at = self.self_info.at or self.at
        else:
            raise PyGplusErrors('atがありません。get_user_info()を実行するかAPIHandlerにatを引数に入れてください。')
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

    ################################ 未実装API ################################

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



    