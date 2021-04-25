import requests

class PublicProfile():
    """Returned when fetching a public profile using `ByteAPI.account(<Account ID>)`"""
    def __init__(self, session: requests.Session, user_id: str, token: str):
        try:
            self.userData = session.get("https://api.byte.co/account/id/" + str(user_id), headers={ "Authorization": token }).json()["data"]
            self.user_id = self.userData["id"]
            self.username = self.userData["username"]
            """Username of the target user"""
            self.display_name = self.userData["displayName"]
            """Displayname of the target user"""
            self.avatar_url = self.userData["avatarURL"]
            self.bio = self.userData["bio"]
            self.is_following = self.userData["isFollowing"]
            self.is_followed = self.userData["isFollowed"]
            self.is_blocked = self.userData["isBlocked"]
            self.can_message = self.userData["canMessage"]
            self.__token = token
            self.__rsess = session
        except:
            raise Exception("Unable to find user (ID: "+str(user_id)+")")

    def follow(self):
        """Follow the account"""
        res = self.__rsess.put("https://api.byte.co/account/id/"+str(self.user_id)+"/follow", headers={ "Authorization": self.__token })
        print(res.json())
        self.__init__(self.__rsess,self.user_id, self.__token)

    def unfollow(self):
        """Unfollow the account"""
        res = self.__rsess.delete("https://api.byte.co/account/id/"+str(self.user_id)+"/follow", headers={ "Authorization": self.__token })
        self.__init__(self.__rsess,self.user_id, self.__token)

    def rebytes(self):
        """Get all rebytes of the account"""
        res = self.__rsess.get(("https://api.byte.co/account/id/"+str(self.user_id)+"/rebytes"), headers={ "Authorization": self.__token }).json()
        return res["data"]

    def posts(self):
        """Get all posts of the account"""
        res = self.__rsess.get(("https://api.byte.co/account/id/"+str(self.user_id)+"/posts"), headers={ "Authorization": self.__token }).json()
        return res["data"]