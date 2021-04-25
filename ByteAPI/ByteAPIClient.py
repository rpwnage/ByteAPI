from __future__ import annotations
import requests
import json
from ByteAPI.PublicProfile import PublicProfile
from ByteAPI.Post import PublicPost
from ByteAPI.Conversation import Conversation

class AuthenticationError(Exception):
    def __init__(self, token):
        super().__init__("Unable to authenticate with given token ("+str(token)+")")

class APIError(Exception):
    def __init__(self, message):
        super().__init__(str(message))

def handleResponseError(self, response):
    """
    This function checks the respoonse of a API request for potential errors
    """
    if response.status_code == 401:
        raise AuthenticationError(self.__token)
    if "success" in response.json():
        if int(response.json()["success"]) != 1:
            raise APIError(str(response.json()["error"]["message"]))
        if int(response.json()["success"]) == 1:
            return True
    return True

class ByteAPI:
    def __init__(self, token):
        """Create a new ByteAPI Client instance from `token`"""
        self.__token = token
        self.__rsess = requests.Session()
        self.user_info = self.__accountInfo()
        self.username = self.user_info["username"]
        """Username of the Authenticated user"""
        self.user_id = self.user_info["id"]
        """UserID of the Authenticated user"""
        self.following = self.__accountFollowing()
        self.following_count = self.user_info["followingCount"]
        self.follower = self.__accountFollowing()
        self.follower_count = self.user_info["followerCount"]
        self.loop_count = self.user_info["loopCount"]
        self.consumed_loops_count = self.user_info["loopsConsumedCount"]
        self.profile_backgroundColor = self.user_info["backgroundColor"]
        self.profile_foregroundColor = self.user_info["foregroundColor"]
        self.conversations = self.__conversations()

    def __conversations(self):
        ret = []
        res = self.__rsess.post("https://api.byte.co/dm-get-conversations", headers={ "Authorization": self.__token }, json={}).json()
        for conversation in res["data"]["conversations"]:
            ret.append(Conversation(self.__rsess, self.__token, conversation["id"], conversation["messages"], conversation["members"]))
        return ret

    def __accountInfo(self):
        res = self.__rsess.get("https://api.byte.co/account/me", headers={"Authorization": self.__token})
        handleResponseError(self, res)
        return res.json()["data"]

    def __accountFollowing(self):
        res = self.__rsess.get("https://api.byte.co/account/me/following", headers={"Authorization": self.__token})
        handleResponseError(self, res)
        return res.json()["data"]

    def __accountFollowers(self):
        res = self.__rsess.get("https://api.byte.co/account/me/followers", headers={"Authorization": self.__token})
        handleResponseError(self, res)
        return res.json()["data"]

    def findAccount(self, account_id: str) -> PublicProfile:
        """Get a `PublicProfile` object by account_id"""
        profile = PublicProfile(self.__rsess, self.__token, account_id)
        return profile

    def findPost(self, post_id: str) -> PublicPost:
        """Get a `PublicPost` object by post_id"""
        post = PublicPost(self.__rsess, post_id, self.__token)
        return post

    def changeUsername(self, username: str):
        """Change your own username"""
        res = self.__rsess.put("https://api.byte.co/account/me", headers={ "Authorization": self.__token }, json={ "username": str(username) })
        return handleResponseError(self, res)

    def changeDisplayname(self, display_name: str):
        """Change your own displayname"""
        res = self.__rsess.put("https://api.byte.co/account/me", headers={ "Authorization": self.__token }, json={ "displayName": str(display_name) })
        return handleResponseError(self, res)

    def changeColorScheme(self, color_scheme: int):
        """
        Change your profiles color scheme. `color_scheme` has to be one of the existing color schemes which can be fetched with `colorSchemes(self)`
        """
        if int(color_scheme) in range(0, len(self.colorSchemes()["colors"])):
            res = self.__rsess.put("https://api.byte.co/account/me", headers={ "Authorization": self.__token }, json={ "colorScheme": int(color_scheme) })
            return handleResponseError(self, res)
        raise APIError("Unknown Color scheme ("+str(color_scheme)+")")

    def colorSchemes(self):
        """Get a list of available color schemes which can be used to set your user profiles color scheme."""
        res = self.__rsess.get("https://api.byte.co/account/me/colors", headers={ "Authorization": self.__token })
        handleResponseError(self, res)
        return res.json()["data"]

    def postComment(self, post_id, text: str):
        """Post a comment under a post by post_id with the contents of text"""
        res = self.__rsess.post(("https://api.byte.co/post/id/"+str(post_id)+"/feedback/comment"), headers={ "Authorization": self.__token }, json={ "postID": str(post_id), "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "body": str(text)})
        handleResponseError(self, res)
        return res.json()["data"]

    def deleteComment(self, comment_id):
        """Delete a existing comment by comment_id"""
        res = self.__rsess.post(("https://api.byte.co/feedback/comment/id/" + str(comment_id)), headers={ "Authorization": self.__token }, json={ "commentID": str(comment_id) })
        return handleResponseError(self, res)

    def likeComment(self, comment_id):
        """Like a comment by comment_id"""
        res = self.__rsess.put(("https://api.byte.co/feedback/comment/id/"+str(comment_id)+"/feedback/like"), headers={ "Authorization": self.__token })
        return handleResponseError(self, res)

    def dislikeComment(self, comment_id):
        """Dislike a comment by comment_id"""
        res = self.__rsess.delete(("https://api.byte.co/feedback/comment/id/"+str(comment_id)+"/feedback/like"), headers={ "Authorization": self.__token })
        return handleResponseError(self, res)

    def postCommentReply(self, comment_id, text: str):
        """Reply to a existing comment by comment_id"""
        res = self.__rsess.post(("https://api.byte.co/feedback/comment/id/"+str(comment_id)+"/feedback/comment"), headers={ "Authorization": self.__token }, json={ "postID": str(comment_id).split("-")[0], "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "body": str(text)})
        handleResponseError(self, res)
        return res.json()["data"]