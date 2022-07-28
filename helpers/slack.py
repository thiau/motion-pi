import requests
import json
import logging
import os
from dotenv import load_dotenv


load_dotenv()


class Slack:
    def __init__(self):
        self.send_api_endpoint = os.getenv("SLACK_SEND_API_ENDPOINT")
        self.update_api_endpoint = os.getenv("SLACK_UPDATE_API_ENDPOINT")
        self.api_token = os.getenv("SLACK_API_TOKEN")
        self.default_channel = os.getenv("SLACK_DEFAULT_CHANNEL")

        # Logging setup
        logging.basicConfig(level=logging.INFO,
                            format='%(levelname)s - %(asctime)s - %(message)s')
        logging.getLogger('slack_helper.py')

    def get_headers(self):
        headers = dict()
        headers["Authorization"] = f'Bearer {self.api_token}'
        headers["Content-Type"] = 'application/json'
        return headers

    def build_payload(self, message, channel=None, ts=None):
        payload = dict()
        payload["channel"] = channel
        payload["text"] = message
        payload["thread_ts"] = ts
        return json.dumps(payload)

    def send_message(self, message=None, channel=None, thread_ts=None, custom_payload=None):
        try:
            channel = self.default_channel if not channel else channel
            payload = custom_payload if custom_payload else self.build_payload(
                message, channel, thread_ts)
            headers = self.get_headers()

            response = requests.post(
                self.send_api_endpoint, headers=headers, data=payload)
            response = json.loads(response.text)

            if response.get("ok"):
                return response
            else:
                raise Exception(response.get("error"))
        except Exception as err:
            logging.error("Error on sending slack message")
            logging.error(err)

    def update_message(self, message=None, channel=None, ts=None, custom_payload=None):
        try:
            channel = self.default_channel if not channel else channel
            payload = custom_payload if custom_payload else self.build_payload(
                message, channel, ts)
            headers = self.get_headers()

            response = requests.post(
                self.update_api_endpoint, headers=headers, data=payload)
            response = json.loads(response.text)

            if response.get("ok"):
                return response
            else:
                raise Exception(response.get("error"))
        except Exception as err:
            logging.error("Error on update slack message")
            logging.error(err)