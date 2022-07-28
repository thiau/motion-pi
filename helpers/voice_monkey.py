import requests
import os

class VoiceMonkey:
    def __init__(self, access_token = None, secret_token = None):
        self.access_token = access_token if access_token else os.getenv("MONKEY_ACCESS_TOKEN")
        self.secret_token = secret_token if secret_token else os.getenv("MONKEY_SECRET_TOKEN")

    def trigger_monkey(self, monkey_id: str):
        base_url="https://api.voicemonkey.io/trigger"
        url = f"{base_url}?access_token={self.access_token}&secret_token={self.secret_token}&monkey={monkey_id}"
        requests.get(url)