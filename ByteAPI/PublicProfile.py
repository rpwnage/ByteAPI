import requests

class PublicProfile():
    """Returned when fetching a public profile using `ByteAPI.account(<Account ID>)`"""
    def __init__(self, session: requests.Session, token: str, user_id: str):
        try:
            self.__rsess = session
            self.__token = token
            self.user_data = self.__rsess.get("https://api.byte.co/account/id/" + str(user_id), headers={ "Authorization": self.__token }).json()["data"]
            self.user_id = self.user_data["id"]
            self.username = self.user_data["username"]
            """Username of the target user"""
            self.display_name = self.user_data["displayName"]
            """Displayname of the target user"""
            if "avatarURL" in self.user_data:
                self.avatar_url = self.user_data["avatarURL"]
                """URL to the users avatar (if exists)"""
            if "bio" in self.user_data:
                self.bio = self.user_data["bio"]
                """Biography of the user (if exists)"""
            if "preferences" not in self.user_data:
                self.is_following = self.user_data["isFollowing"]
                self.is_followed = self.user_data["isFollowed"]
                self.is_blocked = self.user_data["isBlocked"]
                self.can_message = self.user_data["canMessage"]
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