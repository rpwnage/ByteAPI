import requests

class Message:
    def __init__(self, session: requests.Session, token: str, message_id: str, conversation_id: str, author_id: str, body: dict):
        self.__token = token
        self.__rsess = session
        self.message_id = message_id
        self.conversation_id = conversation_id
        self.author = PublicProfile(self.__rsess, self.__token, author_id)
        self.text = body["text"]
        self.type = body["type"]

class Conversation:
    def __init__(self, session: requests.Session, token: str, conversation_id: str, messages: list, members: list):
        """This represents a direct-message conversation between two users"""
        self.__token = token
        self.__rsess = session
        self.id = conversation_id
        self.messages = []
        for message in messages:
            self.messages.append(Message(self.__rsess, self.__token, message["id"], message["conversationID"], message["authorID"], message["body"]))
        self.members = []
        for member in members:
            self.members.append(PublicProfile(self.__rsess, self.__token, member))