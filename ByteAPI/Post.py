import requests
from ByteAPI.PublicProfile import PublicProfile
from ByteAPI.Community import Community

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

class DraftPost:
    def __init__(self, session: requests.Session, thumbnail_upload_id: str, video_upload_id: str, allow_remix: bool, caption: str, duration: float, token: str):
        """Used to create/publish posts within the API"""
        try:
            self.__rsess = session
            self.__token = token
            self.thumbnail_upload_id = thumbnail_upload_id
            self.video_upload_id = video_upload_id
            self.allow_remix = allow_remix
            self.caption = caption
            self.duration = duration
        except Exception as err:
            raise Exception("Unable to create draft ("+str(err)+")")
        
    def publish(self):
        """Publishes the data saved in the Used DraftPost instance and returns `PublicPost` for the published Post"""
        res = self.__rsess.post("https://api.byte.co/post", headers={ "Authorization": self.__token }, json={
            "thumbUploadID": self.thumbnail_upload_id, 
            "allowRemix": self.allow_remix,
            "soundTitle": None,
            "videoUploadID": self.video_upload_id,
            "composition": {
                "text": [],
                "footageTypes": [],
                "imageCount": 0,
                "clips": [
                    {
                        "isFromCameraRoll": False,
                        "duration":self.duration,
                        "isFrontFacingCamera": False
                    },
                    {
                        "isFromCameraRoll": False,
                        "duration": self.duration,
                        "isFrontFacingCamera": False
                    }
                ]
            },
            "caption": self.caption,
            "soundArtworkUploadID":None,
            "soundParentID":None
        }).json()
        
        if res["success"] == 1:
            return PublicPost(self.__rsess, res["data"]["id"], self.__token)

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
            self.author = PublicProfile(self.__rsess, self.__token, self.post_data["authorID"])
            self.curation_allowed = bool(self.post_data["allowCuration"])
            self.remix_allowed = bool(self.post_data["allowRemix"])
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
            if "animatedThumbnail" in self.post_data:
                self.animated_thumbnail_source = str(self.post_data["animatedThumbnail"])
            if "watermarkedVideo" in self.post_data:
                self.watermarked_video_source = str(self.post_data["watermarkedVideo"])
            self.media = PostMedia(self.__rsess, self.id, self.__token)
            if "category" in self.post_data:
                self.category = str(self.post_data["category"])
                self.community = Community(self.__rsess, self.post_data["community"]["id"], self.__token)
        except Exception as err:
            raise Exception("Unable to find post (ID: "+str(post_id)+")")

    def like(self):
        """Like the post"""
        res = self.__rsess.put(("https://api.byte.co/post/id/"+str(self.id)+"/feedback/like"), headers={ "Authorization": self.__token }, json={ "_context": { "isZenMode": False }, "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "postID": str(self.id) }).json()
        if "success" in res:
            if res["success"] == 1:
                self.__init__(self.__rsess, self.id, self.__token)

    def dislike(self):
        """Dislike the post"""
        res = self.__rsess.delete(("https://api.byte.co/post/id/"+str(self.id)+"/feedback/like"), headers={ "Authorization": self.__token }, json={ "_context": { "isZenMode": False }, "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}", "postID": str(self.id) }).json()
        if "success" in res:
            if res["success"] == 1:
                self.__init__(self.__rsess, self.id, self.__token)

    def similar(self):
        """Find similar posts"""
        res = self.__rsess.post("https://api.byte.co/post/id/"+str(self.id)+"/similar", headers={ "Authorization": self.__token }, json={ "metadata": "{\"source\":\"feed:your_mix::collection:popularNow\"}" })
        print(res.json()["data"])

    def rebyte(self):
        """Rebyte the post"""
        res = self.__rsess.post("https://api.byte.co/rebyte", headers={ "Authorization": self.__token }, json={ "postID": str(self.id), "metadata": "{\"source\":\"feed:your_mix::collection:popularThisMonth\"}" }).json()
        if res["success"] == 0:
            if res["error"]["code"] == 2002:
                self.__init__(self.__rsess, self.id, self.__token)
                return True

    def unrebyte(self):
        """Un-rebyte the post"""
        res = self.__rsess.delete(("https://api.byte.co/post/id/"+str(self.id)+"/rebyte"), headers={ "Authorization": self.__token }).json()
        if res["success"] == 1:
            self.__init__(self.__rsess, self.id, self.__token)
            return True
