# -*- coding:utf-8 -*-

from pygplus.utils import Utils
from pygplus.errors import PyGplusErrors

json_lib = Utils.import_simplejson()

class Model(object):
    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        pickle = dict(self.__dict__)
        try:
            del pickle['_api']
        except KeyError:
            pass
        return pickle

    @classmethod
    def parse(cls,method,data):
        raise NotImplementedError

class Comments(Model):
    @classmethod
    def parse(cls,method,data):
        comments = cls.parse_list(method,data)
        return comments

    @classmethod
    def parse_list(cls,method,data_list):
        api = method.api
        results = []
        for comment_json in data_list:
            cmt = cls(api)
            setattr(cmt,'author',comment_json[1])
            setattr(cmt,'body',comment_json[5])
            setattr(cmt,'timestamp',Utils.conv_jsdate2datetime(comment_json[3]))
            setattr(cmt,'comment_id',comment_json[4])
            setattr(cmt,'author_id',comment_json[6])
            setattr(cmt,'item_id',comment_json[7])
            setattr(cmt,'author_icon_url','https:'+comment_json[16])
            results.append(cmt)
        return results

class Posts(Model):
    @classmethod
    def parse(cls,method,data):
        posts = cls.parse_list(method,data)
        return posts

    @classmethod
    def parse_list(cls,method,data_list):
        api = method.api
        results = []
        for post_json in data_list:
            pst = cls(api)
            setattr(pst,'author',post_json[3])
            setattr(pst,'author_id',post_json[5])
            setattr(pst,'body',post_json[4])
            setattr(pst,'timestamp',Utils.conv_jsdate2datetime(post_json[5]))
            setattr(pst,'post_id',post_json[21])
            setattr(pst,'item_id',post_json[8])
            if post_json[7] != None and post_json[7] != []:
                comments = Comments.parse(method,post_json[7])
            else:
                comments = []
            setattr(pst,'comments',comments)
            media = {}
            if post_json[11] != None and post_json[11] != []:
                media_type = post_json[11][0][24][4]
                media['type'] = media_type
                if media_type == 'image':
                    images = []
                    for images_json in post_json[11]:
                        image = {
                            'image_url':images_json[5][1],
                            'height':images_json[5][2],
                            'width':images_json[5][3],
                            'filename':images_json[21],
                            'album_url':images_json[24][1],
                            'mimetype':images_json[24][3],
                        }
                        images.append(image)
                    media['images'] = images

                elif media_type == 'video':
                    video_json = post_json[11]
                    video = {
                        'title':video_json[0][3],
                        'swf_url':video_json[0][5][1],
                        'description':video_json[0][21],
                        'original_url':video_json[0][24][1],
                        'mimetype':video_json[0][24][3],
                    }
                    thumbnails = []
                    if video_json[0][41] != None and video_json[0][41] != []:
                        for thumbnail_json in video_json[0][41]:
                            thumbnail = {
                                'url': thumbnail_json[1]
                            }
                            if len(thumbnail_json) >= 3:
                                thumbnail['height'] = thumbnail_json[2]
                                thumbnail['width'] = thumbnail_json[3]
                            thumbnails.append(thumbnail)
                    video['thumbnails'] = thumbnails
                    media['video'] = video
                elif media_type == 'document':
                    document_json = post_json[11]
                    document = {
                        'title':document_json[0][3],
                        'description':document_json[0][21],
                        'site_url':document_json[0][24][1],
                    }
                    favicons = []
                    if document_json[0][41] != None and document_json[0][41] != []:
                        for favicon_json in document_json[0][41]:
                            favicons.append(favicon_json[1])
                    document['favicon'] = favicons
                    media['document'] = document
                else:
                    media[media_type] = post_json[11]
                setattr(pst,'media',media)
            shares = []
            if post_json[25] != None and post_json[25] != []:
                for share_json in post_json[25]:
                    share = {
                        'screen_name': share_json[0],
                        'user_id': share_json[1],
                    }
                    shares.append(share)
            setattr(pst,'shares',shares)
            plusones = []
            if post_json[73] != None and post_json[73] != []:
                if post_json[73][17] != None and post_json[73][17] != []:
                    for plusone_json in post_json[73][17]:
                        plusone = {
                            'screen_name': plusone_json[0],
                            'user_id': plusone_json[1],
                            'user_icon_url': plusone_json[3],
                            }
                        plusones.append(plusone)
            setattr(pst,'plusones',plusones)
            results.append(pst)
        return results

class UserInfo(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        userinfo = cls(api)
        scripts = Utils.extract_initdata_json_string_list(data)
        for script in scripts:
            json = json_lib.loads(script['data'])
            if script['key'] == '5':
                setattr(userinfo,'user_id',json[0])
                setattr(userinfo,'user_icon_url','https:'+json[2][3])
                setattr(userinfo,'first_name',json[2][4][1])
                setattr(userinfo,'family_name',json[2][4][2])
                setattr(userinfo,'screen_name',json[2][4][3])
                setattr(userinfo,'other_names',json[2][5][1][0][0])
                setattr(userinfo,'occupation',json[2][6][1])
                setattr(userinfo,'places_lived',json[2][9][2][0])
                setattr(userinfo,'introduction',json[2][14][1])
                setattr(userinfo,'tagline',json[2][33][1])
                posts = Posts.parse(method,json[4][0])
                setattr(userinfo,'posts',posts)
            elif script['key'] == '36':
                setattr(userinfo,'country_code',json[0])
            elif script['key'] == '1':
                setattr(userinfo,'at',json[15])
        return userinfo

class PostInfo(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        postinfo = cls(api)
        data = Utils.fix_json_string(data)
        print data
        json = json_lib.loads(data)
        setattr(postinfo,'posts',Posts.parse(method,[json[0][1][1]]))
        return postinfo


class Followers(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        followers = cls(api)
        data = Utils.fix_json_string(data)
        json = json_lib.loads(data)
        setattr(followers,'my_id',json[0][0][1])
        users = []
        for user_json in json[0][1][2]:
            user = {
                'id':user_json[0][2],
                'name':user_json[2][0],
                'icon_url':'https:'+user_json[2][8],
                'lived':user_json[2][11],
                'education':user_json[2][12],
                'career':user_json[2][13],
                'occupation':user_json[2][14],
            }
            if len(user_json[2]) > 19:
                user['brief_description'] = user_json[2][21]
            users.append(user)
        setattr(followers,'users',users)
        return followers

class Circles(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        circles = cls(api)
        data = Utils.fix_json_string(data)
        json = json_lib.loads(data)
        my_id = json[0][0][1]
        circles_list = []
        for circle_json in json[0][1][1]:
            circle = {
                'id':circle_json[0][0],
                'name':circle_json[1][0],
                'description':circle_json[1][2],
            }
            circles_list.append(circle)
        users = []
        for following_json in json[0][1][2]:
            user = {
                'id':following_json[0][2],
                'name':following_json[2][0],
                'icon_url':'https:'+following_json[2][8],
            }
            joined_circle_ids = []
            for joined_circles_json in following_json[3]:
                joined_circle_ids.append(joined_circles_json[2][0])
            user['joined_circle_ids'] = joined_circle_ids
            users.append(user)
        setattr(circles,'my_id',my_id)
        setattr(circles,'circles_list',circles_list)
        setattr(circles,'following_users',users)
        return circles

class UploadPhoto(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        uploadphoto = cls(api)
        json = json_lib.loads(data)
        json_err = json.get("errorMessage",None)
        if json_err:
            raise PyGplusErrors('Failed to upload photo. Request rejected.',json_err)
        else:
            json_photo = json.get("sessionStatus",None)
            if json_photo:
                result = {}
                if json_photo["state"] == 'OPEN':
                    result = {
                        'url':json_photo["externalFieldTransfers"][0]["formPostInfo"]["url"],
                        'upload_id':json_photo["upload_id"],
                        'size':json_photo["externalFieldTransfers"][0]["bytesTotal"],
                        'mimetype':json_photo["externalFieldTransfers"][0]["content_type"],
                    }
                elif json_photo["state"] == 'FINALIZED':
                    result = {
                        'size':json_photo["externalFieldTransfers"][0]["bytesTotal"],
                        'kind':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["kind"],
                        'album_id':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["albumid"],
                        'photo_id':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["photoid"],
                        'width':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["width"],
                        'height':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["height"],
                        'photo_url':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["url"],
                        'filename':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["title"],
                        'description':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["description"],
                        'username':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["username"],
                        'photo_page_url':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["photoPageUrl"],
                        'album_page_url':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["albumPageUrl"],
                        'mimetype':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["mimeType"],
                        'timestamp':Utils.conv_jsdate2datetime(json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["timestamp"]),
                        'auto_downsize':json_photo["additionalInfo"]["uploader_service.GoogleRupioAdditionalInfo"]["completionInfo"]["customerSpecificInfo"]["autoDownsized"],
                    }
                setattr(uploadphoto,'photo',result)
        return uploadphoto

class UploadLink(Model):
    @classmethod
    def parse(cls,method,data):
        json = json_lib.loads(Utils.fix_json_string(data))
        result = {
            'type':'link',
        }
        if len(json[0][2]) >= 1:
            if len(json[0][2]) > 5:
                result['result'] = json[0][2][5]
            else:
                result['result'] = json[0][2][0]
        return result

class UploadVideoLink(Model):
    @classmethod
    def parse(cls,method,data):
        json = json_lib.loads(Utils.fix_json_string(data))
        result = {
            'type':'video',
        }
        if len(json[0][3]) >= 1:
            result['result'] = json[0][3][0]
        return result

class Notifications(Model):
    AddBack = 'AddBack' # フォロー返し
    Add = 'Add' # フォロー
    Reply = 'Reply' # コメント・共有・+1された
    @classmethod
    def parse(cls,method,data):
        api = method.api
        ntfcs = cls(api)
        data = Utils.fix_json_string(data)
        json = json_lib.loads(data)
        notifications = []
        my_user_id = json[0][0][1]
        for notification_json in json[0][1][1][0]:
            ntfc = cls(api)
            if notification_json[10] == 'g:'+my_user_id and notification_json[17] == '0g:'+my_user_id:
                users = []
                for user_json in notification_json[2][0][1]:
                    #user_gender = user_json[2][4]
                    user = {
                        'user_id':user_json[6],
                        'screen_name':user_json[2][0],
                        'user_icon_url':user_json[2][2],
                        }
                    users.append(user)
                setattr(ntfc,'users',users)
                setattr(ntfc,'flag',Notifications.Add)
            elif notification_json[10] == 'g:'+my_user_id+':add-back' and notification_json[17] == '0g:'+my_user_id+':add-back':
                users = []
                for user_json in notification_json[2][0][1]:
                    #user_gender = user_json[2][4]
                    user = {
                        'user_id':user_json[6],
                        'screen_name':user_json[2][0],
                        'user_icon_url':user_json[2][2],
                        }
                    users.append(user)
                setattr(ntfc,'users',users)
                setattr(ntfc,'flag',Notifications.Add)
            else:
                # TODO: Comment, Share, +1 の細分化。
                # 下記から通知を送ったユーザは取得できるが、コメントの場合はコメント本文は取得できない。
                #[2][0]: Comment
                #[2][1]: +1
                #[2][2]: Share
                setattr(ntfc,'posts',None)
                if notification_json[18] != None and notification_json[18] != []:
                    if notification_json[18][0] != None and notification_json[18][0] != []:
                        if notification_json[18][0][0] != None and notification_json[18][0][0] != []:
                            posts = Posts.parse(method,[notification_json[18][0][0]])
                            setattr(ntfc,'posts',Posts)
                setattr(ntfc,'flag',Notifications.Reply)
            notification_user_ids = []
            for user_id in notification_json[19]:
                notification_user_ids.append(user_id)
            setattr(ntfc,'notification_user_ids',notification_user_ids)
            notifications.append(ntfc)
        setattr(ntfcs,'notifications',notifications)
        users_details = []
        for users_details_json in json[0][1][1][8]:
            user = cls(api)
            setattr(user,'screen_name',users_details_json[0])
            setattr(user,'user_icon_url',users_details_json[2])
            setattr(user,'user_id',users_details_json[3])
            users_details.append(user)
        setattr(ntfcs,'users_details',users_details)
        return ntfcs

class Dashboard(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        dashboard = cls(api)
        scripts = Utils.extract_initdata_json_string_list(data)
        for script in scripts:
            json = json_lib.loads(script['data'])
            if script['key'] == '4':
                posts = Posts.parse(method,json[0])
                setattr(dashboard,'posts',posts)
                setattr(dashboard,'next_id',json[1])
                setattr(dashboard,'next_obj',json[2])
        return dashboard

class NextPostsData(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        nextdata = cls(api)
        json = json_lib.loads(Utils.fix_json_string(data))
        posts = Posts.parse(method,json[0][1][1][0])
        setattr(nextdata,'posts',posts)
        setattr(nextdata,'next_id',json[0][1][1][1])
        setattr(nextdata,'next_obj',json[0][1][1][2])
        return nextdata

class HoverCards(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        hovercards = cls(api)
        data = Utils.fix_json_string(data)
        json = json_lib.loads(data)
        setattr(hovercards,'user_id',json[0][1][1][0][1][0][2])
        setattr(hovercards,'screen_name',json[0][1][1][0][1][2][0])
        setattr(hovercards,'user_icon_url','https:'+json[0][1][1][0][1][2][8])
        setattr(hovercards,'places_lived',json[0][1][1][0][1][2][11])
        setattr(hovercards,'employment',json[0][1][1][0][1][2][13])
        setattr(hovercards,'occupation',json[0][1][1][0][1][2][14])
        setattr(hovercards,'tagline',json[0][1][1][0][1][2][21])
        #setattr(hovercards,'',json[0][1][1][0][2][][])# users
        return hovercards

class UpdatePost(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        updatepost = cls(api)
        data = Utils.fix_json_string(data)
        json = json_lib.loads(data)
        posts = Posts.parse(method,json[0][1][1][0])
        setattr(updatepost,'unknown_obj1',json[0][1][2][0])
        setattr(updatepost,'unknown_obj2',json[0][1][2][1])
        setattr(updatepost,'posts',posts)
        return updatepost

class UpdateComment(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        updatecomment = cls(api)
        data = Utils.fix_json_string(data)
        json = json_lib.loads(data)
        comments = Comments.parse(method,[json[0][1][1]])
        setattr(updatecomment,'comments',comments)
        return updatecomment


class JsonRaw(Model):
    @classmethod
    def parse(cls,method,data):
        data = Utils.fix_json_string(data)
        print data
        return json_lib.loads(data)

class Raw(Model):
    @classmethod
    def parse(cls,method,data):
        return data

class ModelFactory(object):
    userinfo = UserInfo
    postinfo = PostInfo
    notifications = Notifications
    followers = Followers
    circles = Circles
    notifications = Notifications
    uploadphoto = UploadPhoto
    uploadlink = UploadLink
    uploadvideolink = UploadVideoLink
    dashboard = Dashboard
    nextpostsdata = NextPostsData
    hovercards = HoverCards
    updatepost = UpdatePost
    updatecomment = UpdateComment
    jsonraw = JsonRaw
    raw = Raw
