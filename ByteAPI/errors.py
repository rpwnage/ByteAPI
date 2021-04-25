class AuthenticationError(Exception):
    def __init__(self, token):
        super().__init__("Unable to authenticate with given token ("+str(token)+")")

class APIError(Exception):
    def __init__(self, message):
        super().__init__(str(message))

def handleResponseError(self, response):
    if response.status_code == 401:
        raise AuthenticationError(self.token)
    if "success" in response.json():
        if int(response.json()["success"]) != 1:
            raise APIError(str(response.json()["error"]["message"]))
    return True