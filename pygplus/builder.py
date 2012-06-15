# -*- coding:utf-8 -*-

from datetime import datetime
import time
import os

import simplejson as json_lib

from pygplus.utils import Utils
from pygplus.errors import PyGplusErrors

__all__ = ['Builder']

class Builder(object):
    ANYONE = 1 # 一般公開
    EXTENDED = 2 # 友だちの友だちサークル公開
    CIRCLES = 3 # 限定公開
    LIMITED = 4 # サークル指定
    @staticmethod
    def build_post_json(message,user_id,scope_data,album_id=None,media_json=None,share=False,comment=False):
        """
        Description...
        Args:
            none
        Retruns:
            none
        Exceptions:
            none
        """
        if not media_json:
            media_json = "[]"
        if album_id:
            end_bool = True
        else:
            end_bool = False
        post_json = [
            message,
            "oz:"+user_id+'.'+str(time.mktime(datetime.now().timetuple())),
            None,
            album_id,
            None,
            None,
            media_json,
            None,
            scope_data,
            True,
            [],
            False,
            False,
            None,
            [],
            None,
            False,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            comment,
            share,
            end_bool,
            None,
            None,
            None,
            None,
            None,
            None,
            []
        ]
        return json_lib.dumps(post_json)

    @staticmethod
    def __build_scope_circle(scope_data,scope_type,name,_id,me,requires_key,group_type):

        scope_data.append(
            {
                "scope":{
                    "scopeType":scope_type,
                    "name":name,
                    "id":_id,
                    "me":me,
                    "requiresKey": requires_key,
                    "groupType":group_type
                },
                "role":20
            }
        )
        scope_data.append(
            {
                "scope":{
                    "scopeType":scope_type,
                    "name":name,
                    "id":_id,
                    "me":me,
                    "requiresKey": requires_key,
                    "groupType":group_type
                },
                "role":60
            }
        )
        return scope_data

    @staticmethod
    def __build_scope_reply_user(scope_data,icon_url,scope_type,name,_id,me,requires_key,is_me):
        scope_data.append(
            {
                "scope":{
                    "iconUrl":icon_url,
                    "scopeType":scope_type,
                    "name":name,
                    "id":_id,
                    "me":me,
                    "requiresKey": requires_key,
                    "isMe":is_me
                },
                "role":20
            }
        )
        scope_data.append(
            {
                "scope":{
                    "iconUrl":icon_url,
                    "scopeType":scope_type,
                    "name":name,
                    "id":_id,
                    "me":me,
                    "requiresKey": requires_key,
                    "isMe":is_me
                },
                "role":60
            }
        )
        return scope_data

    @staticmethod
    def build_scope_data(api,scope_type,user_id,circle_ids=[],reply_user_ids=[]):
        """
        Description...
        Args:
            scope_type: select Builder.ANYONE, Builder.EXTENDED, Builder.LIMITED
                Builder.ANYONEを選択された場合circle_idsは無視されます。
        Retruns:
            none
        Exceptions:
            none
        """
        scope_data = []
        if scope_type == Builder.ANYONE: # 一般公開
            name = 'Anyone'
            _id = 'anyone'
            _scope_type = 'anyone'
            me = True
            requires_key = False
            group_type = None
            Builder.__build_scope_circle(scope_data,_scope_type,name,_id,me,requires_key,group_type)
        elif scope_type == Builder.EXTENDED: # 友達の友達サークル
            name = 'Extendedcircles'
            _id = user_id+'.1f'
            _scope_type = 'focusGroup'
            me = False
            requires_key = False
            group_type = 'e'
            Builder.__build_scope_circle(scope_data,_scope_type,name,_id,me,requires_key,group_type)
        elif scope_type == Builder.CIRCLES: # 限定公開
            name = 'Yourcircles'
            _id = user_id+'.1c'
            _scope_type = 'focusGroup'
            me = False
            requires_key = False
            group_type = 'a'
            Builder.__build_scope_circle(scope_data,_scope_type,name,_id,me,requires_key,group_type)
        elif scope_type == Builder.LIMITED: # サークル指定
            if circle_ids == None and circle_ids == []:
                raise PyGplusErrors('circle_idsがありません。LIMITEDオプションはこれを必要としています。')
            name = 'anonymous'
            _scope_type = 'focusGroup'
            me = False
            requires_key = False
            group_type = 'p'
            for circle_id in circle_ids:
                _id = user_id+'.'+circle_id
                Builder.__build_scope_circle(scope_data,_scope_type,name,_id,me,requires_key,group_type)
        else:
            # 該当しない場合は限定公開
            name = 'Yourcircles'
            _id = user_id+'.1c'
            _scope_type = 'focusGroup'
            me = False
            requires_key = False
            group_type = 'a'
            Builder.__build_scope_circle(scope_data,_scope_type,name,_id,me,requires_key,group_type)
        if reply_user_ids != None or reply_user_ids != []:
            scope_type = 'user'
            is_me = False
            for reply_user_id in reply_user_ids:
                # TODO: APIを呼ばなくてもCacheされたもののなかに無いか確認する
                user = api.lookup_hovercards(user_id=reply_user_id)
                icon_url = user.user_icon_url
                name = user.screen_name
                Builder.__build_scope_reply_user(scope_data=scope_data,icon_url=icon_url,scope_type=scope_type,name=name,_id=reply_user_id,me=me,requires_key=requires_key,is_me=is_me)

        scope = {
            "aclEntries":scope_data
        }

        return json_lib.dumps(scope)
    
    @staticmethod
    def build_photo_json(filename,fsize):
        filename = os.path.basename(filename)
        photo_json = {
            "protocolVersion": "0.8",
            "createSessionRequest": {
                "fields": [
                    {
                        "external": {
                            "name": "file",
                            "filename": filename,
                            "formPost": {},
                            "size": fsize
                        },
                    },
                    {
                        "inlined": {
                            "name": "batchid",
                            "content": Utils.get_jsdate_now(),
                            "contentType": "text/plain"
                        }
                    },
                    {
                        "inlined": {
                            "name": "client",
                            "content": "sharebox",
                            "contentType": "text/plain"
                        }
                    },
                    {
                        "inlined": {
                            "name": "disable_asbe_notification",
                            "content": "true",
                            "contentType": "text/plain"
                        }
                    },
                    {
                        "inlined": {
                            "name": "streamid",
                            "content": "updates",
                            "contentType": "text/plain"
                        }
                    },
                    {
                        "inlined": {
                            "name": "use_upload_size_pref",
                            "content": "true",
                            "contentType": "text/plain"
                        }
                    }
                ]
            }
        }
        return json_lib.dumps(photo_json)

    @staticmethod
    def build_media_json(media):
        if media['type'] == 'photos':
            media_json = []
            for media_result in media['result']:
                album_id = media_result.photo['album_id']
                photo_id = media_result.photo['photo_id']
                height = media_result.photo['height']
                width = media_result.photo['width']
                mimetype = media_result.photo['mimetype']
                photo_url = media_result.photo['photo_url']
                filename = media_result.photo['filename']
                photo_page_url = media_result.photo['photo_page_url']
                thumbnail_url = photo_url.replace(filename,'w288-h288/') + filename
                thumbnail_height = 120 # 適当
                thumbnail_width = 120 # 適当
                media_json_pre = [
                    None,
                    None,
                    None,
                    "",
                    None,
                    [
                        None,
                        photo_url,
                        height,
                        width
                    ],
                    None,
                    None,
                    None,
                    [

                    ],
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    filename,
                    None,
                    None,
                    [
                        None,
                        photo_page_url,
                        None,
                        mimetype,
                        "image"
                    ],
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    [
                        # 同じ物を2つ
                        [
                            # photo thumbnails
                            None,
                            thumbnail_url,
                            thumbnail_height,
                            thumbnail_width
                        ],
                        [
                            # photo thumbnails
                            None,
                            thumbnail_url,
                            thumbnail_height,
                            thumbnail_width
                        ],
                    ],
                    None,
                    None,
                    None,
                    None,
                    None,
                    [
                        [
                            None,
                            "picasa",
                            "http://google.com/profiles/media/provider",
                            ""
                        ],
                        [
                            None,
                            "albumid="+album_id+"&photoid="+photo_id,
                            "http://google.com/profiles/media/onepick_media_id",
                            ""
                        ]
                    ]
                ]
                media_json.append(json_lib.dumps(media_json_pre))
            return json_lib.dumps(media_json)

        elif media['type'] == 'link':
            return json_lib.dumps([json_lib.dumps(media['result'])])
        elif media['type'] == 'video':
            return json_lib.dumps([json_lib.dumps(media['result'])])
        else:
            pass

    @staticmethod
    def build_nextdata_json(next_id,next_obj):
        data = [
            next_obj,
            next_id
        ]
        fix_json = json_lib.dumps(data)
        import re
        pre = re.compile(r'^\[\[.*\,\s.*\,\s.*\,\s.*\,\s.*(\,\s.*\,)\s.*,\s.*,\s.*,\s.*,\s.*,\s.*,\s.*,\s.*,\s.*,\s.*,\s.*,\s.*,\s.*\]\,\s.*\]')
        m = pre.match(fix_json)
        if m:
            fix_json = fix_json.replace(m.group(1),', ,')
        return fix_json
