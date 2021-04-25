import requests
from .PublicProfile import PublicProfile
from .Community import Community

class PostMedia:
    def __init__(self, session: requests.Session, post_id: str, token: str):
        try:
            self.__rsess = session
            self.__token = token
            self.post_data = self.__rsess.get("https://api.byte.co/post/id/" + str(post_id), headers={ "Authorization": self.__token }).json()["data"]["media"]
            self.source = str(self.post_data["source"]["url"])
            self.duration = int(self.post_data["source"]["duration"])
        except:
            raise Exception("Unable to fetch Media")

class PublicPost:
    def __init__(self, session: requests.Session, post_id: str, token: str):
        """Returned when fetching posts"""
        try:
            self.__rsess = session
            self.__token = token
            self.post_data = self.__rsess.get("https://api.byte.co/post/id/" + str(post_id), headers={ "Authorization": self.__token }).json()["data"]
            self.id = post_id
            self.type = int(self.post_data["type"])
            self.caption = str(self.post_data["caption"])
            self.author = PublicProfile(self.__rsess, self.post_data["authorID"], self.__token)
            self.curation_allowed = bool(self.post_data["allowCuration"])
            self.remix_allowed = bool(self.post_data["allowRemix"])
            self.category = str(self.post_data["category"])
            self.community = Community(self.__rsess, self.post_data["community"]["id"], self.__token)
            self.date = int(self.post_data["date"])
            self.video_source = str(self.post_data["videoSrc"])
            self.thumbnail_source = str(self.post_data["thumbSrc"])
            self.comment_count = int(self.post_data["commentCount"])
            self.like_count = int(self.post_data["likeCount"])
            self.liked_by_me = bool(self.post_data["likedByMe"])
            self.loop_count = int(self.post_data["loopCount"])
            self.rebyted_by_me = bool(self.post_data["rebytedByMe"])
            self.rebyte_count = int(self.post_data["rebyteCount"])
            self.share_url = str(self.post_data["shareURL"])
            self.animated_thumbnail_source = str(self.post_data["animatedThumbnail"])
            self.watermarked_video_source = str(self.post_data["watermarkedVideo"])
            self.media = 
        except:
            raise Exception("Unable to find post (ID: "+str(post_id)+")")

    def 