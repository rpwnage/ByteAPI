from __future__ import annotations
import requests
import json
from .Account import PublicProfile

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
        raise AuthenticationError(self.token)
    if "success" in response.json():
        if int(response.json()["success"]) != 1:
            raise APIError(str(response.json()["error"]["message"]))
        if int(response.json()["success"]) == 1:
            return True
    return True

class ByteAPI:
    def __init__(self, token):
        """Create a new ByteAPI Client instance from `token`"""
        self.token = token
        self.rsession = requests.Session()
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
        """Like a given post by post_id"""
        res = self.rsession.put(("https://api.byte.co/post/id/"+str(post_id)+"/feedback/like"), headers={ "Authorization": self.token }, json={ "_context": { "isZenMode": False }, "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "postID": str(post_id) })
        return handleResponseError(self, res)

    def dislikePost(self, post_id):
        """Dislike a given post by post_id"""
        res = self.rsession.delete(("https://api.byte.co/post/id/"+str(post_id)+"/feedback/like"), headers={ "Authorization": self.token }, json={ "postID": str(post_id) })
        return handleResponseError(self, res)

    def similarPosts(self, post_id):
        """Fetch posts similar to a existing post by post_id"""
        res = self.rsession.post("https://api.byte.co/post/id/"+str(post_id)+"/similar", headers={ "Authorization": self.token }, json={ "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}" })
        handleResponseError(self, res)
        return res.json()["data"]

    def rebytePost(self, post_id):
        """Rebyte a post by post_id"""
        res = self.rsession.post("https://api.byte.co/rebyte", headers={ "Authorization": self.token }, json={ "postID": str(post_id), "metadata": "{\"source\":\"feed:your_mix::collection:popularThisMonth\"}" })
        return handleResponseError(self, res)

    def findAccount(self, account_id) -> PublicProfile:
        """Get information about a account by account_id"""
        profile = PublicProfile(self.rsession, account_id, self.token)
        return profile

    def changeUsername(self, username: str):
        """Change your own username"""
        res = self.rsession.put("https://api.byte.co/account/me", headers={ "Authorization": self.token }, json={ "username": str(username) })
        return handleResponseError(self, res)

    def changeDisplayname(self, display_name: str):
        """Change your own displayname"""
        res = self.rsession.put("https://api.byte.co/account/me", headers={ "Authorization": self.token }, json={ "displayName": str(display_name) })
        return handleResponseError(self, res)

    def changeColorScheme(self, color_scheme: int):
        """
        Change your profiles color scheme. `color_scheme` has to be one of the existing color schemes which can be fetched with `colorSchemes(self)`
        """
        if int(color_scheme) in range(0, len(self.colorSchemes()["colors"])):
            res = self.rsession.put("https://api.byte.co/account/me", headers={ "Authorization": self.token }, json={ "colorScheme": int(color_scheme) })
            return handleResponseError(self, res)
        raise APIError("Unknown Color scheme ("+str(color_scheme)+")")

    def colorSchemes(self):
        """Get a list of available color schemes which can be used to set your user profiles color scheme."""
        res = self.rsession.get("https://api.byte.co/account/me/colors", headers={ "Authorization": self.token })
        handleResponseError(self, res)
        return res.json()["data"]

    def postComment(self, post_id, text: str):
        """Post a comment under a post by post_id with the contents of text"""
        res = self.rsession.post(("https://api.byte.co/post/id/"+str(post_id)+"/feedback/comment"), headers={ "Authorization": self.token }, json={ "postID": str(post_id), "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "body": str(text)})
        handleResponseError(self, res)
        return res.json()["data"]

    def deleteComment(self, comment_id):
        """Delete a existing comment by comment_id"""
        res = self.rsession.post(("https://api.byte.co/feedback/comment/id/" + str(comment_id)), headers={ "Authorization": self.token }, json={ "commentID": str(comment_id) })
        return handleResponseError(self, res)

    def likeComment(self, comment_id):
        """Like a comment by comment_id"""
        res = self.rsession.put(("https://api.byte.co/feedback/comment/id/"+str(comment_id)+"/feedback/like"), headers={ "Authorization": self.token })
        return handleResponseError(self, res)

    def dislikeComment(self, comment_id):
        """Dislike a comment by comment_id"""
        res = self.rsession.delete(("https://api.byte.co/feedback/comment/id/"+str(comment_id)+"/feedback/like"), headers={ "Authorization": self.token })
        return handleResponseError(self, res)

    def postCommentReply(self, comment_id, text: str):
        """Reply to a existing comment by comment_id"""
        res = self.rsession.post(("https://api.byte.co/feedback/comment/id/"+str(comment_id)+"/feedback/comment"), headers={ "Authorization": self.token }, json={ "postID": str(comment_id).split("-")[0], "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "body": str(text)})
        handleResponseError(self, res)
        return res.json()["data"]