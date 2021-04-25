import requests
import json
from .errors import *


class ByteAPI:
    def __init__(self, token):
        self.token = token
        self.rsession = requests.Session()
        self.user_info = self.__accountInfo()
        self.username = self.user_info["username"]
        self.user_id = self.user_info["id"]
        self.following = self.__accountFollowing()
        self.following_count = self.user_info["followingCount"]
        self.follower = self.__accountFollowing()
        self.follower_count = self.user_info["followerCount"]
        self.loop_count = self.user_info["loopCount"]
        self.consumed_loops_count = self.user_info["loopsConsumedCount"]
        self.profile_backgroundColor = self.user_info["backgroundColor"]
        self.profile_foregroundColor = self.user_info["foregroundColor"]

    def __accountInfo(self):
        res = self.rsession.get("https://api.byte.co/account/me", headers={"Authorization": self.token})
        handleResponseError(self, res)
        return res.json()["data"]

    def __accountFollowing(self):
        res = self.rsession.get("https://api.byte.co/account/me/following", headers={"Authorization": self.token})
        handleResponseError(self, res)
        return res.json()["data"]

    def __accountFollowers(self):
        res = self.rsession.get("https://api.byte.co/account/me/followers", headers={"Authorization": self.token})
        handleResponseError(self, res)
        return res.json()["data"]

    def likePost(self, post_id):
        res = self.rsession.put(("https://api.byte.co/post/id/"+str(post_id)+"/feedback/like"), headers={ "Authorization": self.token }, json={ "_context": { "isZenMode": False }, "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "postID": str(post_id) })
        return handleResponseError(self, res)

    def dislikePost(self, post_id):
        res = self.rsession.delete(("https://api.byte.co/post/id/"+str(post_id)+"/feedback/like"), headers={ "Authorization": self.token }, json={ "postID": str(post_id) })
        return handleResponseError(self, res)

    def similarPosts(self, post_id):
        res = self.rsession.post("https://api.byte.co/post/id/"+str(post_id)+"/similar", headers={ "Authorization": self.token }, json={ "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}" })
        handleResponseError(self, res)
        return res.json()["data"]

    def rebytePost(self, post_id):
        res = self.rsession.post("https://api.byte.co/rebyte", headers={ "Authorization": self.token }, json={ "postID": str(post_id), "metadata": "{\"source\":\"feed:your_mix::collection:popularThisMonth\"}" })
        return handleResponseError(self, res)

    def account(self, account_id):
        res = self.rsession.get("https://api.byte.co/account/id/" + str(account_id), headers={ "Authorization": self.token })
        handleResponseError(self, res)
        return res.json()["data"]

    def follow(self, account_id):
        res = self.rsession.put("https://api.byte.co/account/id/"+str(account_id)+"/follow", headers={ "Authorization": self.token })
        return handleResponseError(self, res)

    def unfollow(self, account_id):
        res = self.rsession.delete("https://api.byte.co/account/id/"+str(account_id)+"/follow", headers={ "Authorization": self.token })
        return handleResponseError(self, res) 

    def userRebytes(self, account_id):
        res = self.rsession.get(("https://api.byte.co/account/id/"+str(account_id)+"/rebytes"), headers={ "Authorization": self.token })
        handleResponseError(self, res)
        return res.json()["data"]

    def userPosts(self, account_id):
        res = self.rsession.get(("https://api.byte.co/account/id/"+str(account_id)+"/posts"), headers={ "Authorization": self.token })
        handleResponseError(self, res)
        return res.json()["data"]

    def changeUsername(self, username):
        res = self.rsession.put("https://api.byte.co/account/me", headers={ "Authorization": self.token }, json={ "username": str(username) })
        return handleResponseError(self, res)

    def changeDisplayname(self, display_name):
        res = self.rsession.put("https://api.byte.co/account/me", headers={ "Authorization": self.token }, json={ "displayName": str(display_name) })
        return handleResponseError(self, res)

    def changeColorScheme(self, color_scheme):
        if int(color_scheme) in range(0, len(self.colorSchemes()["colors"])):
            res = self.rsession.put("https://api.byte.co/account/me", headers={ "Authorization": self.token }, json={ "colorScheme": int(color_scheme) })
            return handleResponseError(self, res)
        raise APIError("Unknown Color scheme ("+str(color_scheme)+")")

    def colorSchemes(self):
        res = self.rsession.get("https://api.byte.co/account/me/colors", headers={ "Authorization": self.token })
        handleResponseError(self, res)
        return res.json()["data"]

    def postComment(self, post_id, text):
        res = self.rsession.post(("https://api.byte.co/post/id/"+str(post_id)+"/feedback/comment"), headers={ "Authorization": self.token }, json={ "postID": str(post_id), "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "body": str(text)})
        handleResponseError(self, res)
        return res.json()["data"]

    def deleteComment(self, comment_id):
        res = self.rsession.post(("https://api.byte.co/feedback/comment/id/" + str(comment_id)), headers={ "Authorization": self.token }, json={ "commentID": str(comment_id) })
        return handleResponseError(self, res)

    def likeComment(self, comment_id):
        res = self.rsession.put(("https://api.byte.co/feedback/comment/id/"+str(comment_id)+"/feedback/like"), headers={ "Authorization": self.token })
        return handleResponseError(self, res)

    def dislikeComment(self, comment_id):
        res = self.rsession.delete(("https://api.byte.co/feedback/comment/id/"+str(comment_id)+"/feedback/like"), headers={ "Authorization": self.token })
        return handleResponseError(self, res)

    def postCommentReply(self, comment_id, text):
        res = self.rsession.post(("https://api.byte.co/feedback/comment/id/"+str(comment_id)+"/feedback/comment"), headers={ "Authorization": self.token }, json={ "postID": str(comment_id).split("-")[0], "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "body": str(text)})
        handleResponseError(self, res)
        return res.json()["data"]