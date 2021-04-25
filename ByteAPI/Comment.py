import requests
from .PublicProfile import PublicProfile

class Comment:
    def __init__(self, session: requests.Session, comment_id: str, token: str):
        self.__rsess = session
        self.__token = token
        self.id = comment_id
