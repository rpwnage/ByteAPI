import requests

class Community:
    def __init__(self, session: requests.Session, community_id: str, token: str):
        try:
            self.__rsess = session
            self.__token = token
            self.community_data = self.__rsess.get("https://api.byte.co/community/id/" + str(community_id), headers={ "Authorization": self.__token }).json()["data"]
            self.slug = str(self.community_data["slug"])
            self.description = str(self.community_data["description"])
            self.member_count = int(self.community_data["memberCount"])
            self.video_count = int(self.community_data["videoCount"])
            self.preferred_feed = str(self.community_data["preferredFeed"])
            self.icon = str(self.community_data["icon"])
            self.video = str(self.community_data["video"])
            self.animated_thumbnail = str(self.community_data["animatedThumbnail"])
            self.title = str(self.community_data["title"])
        except:
            raise Exception("Unable to find community (ID: "+str(community_id)+")")