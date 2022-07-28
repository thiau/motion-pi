import logging
import os
import json
from helpers.slack import Slack
from helpers.voice_monkey import VoiceMonkey
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(asctime)s - %(message)s')
logging.getLogger('motion.py')

slack = Slack()

class MotionSense:
    def __init__(self):
        self.lights_on = True
        self.time_window_limit = None
        self.time_window_total_motion = 0
        self.time_window_motion_limit = 3
        self.time_window_seconds = 60
        self.voice_monkey = VoiceMonkey()
        self.slack_message = self.reset_slack_message_template()
        self.slack_ts = None
    
    def reset_slack_message_template(self):
        return {
            "channel": os.getenv("SLACK_DEFAULT_CHANNEL"),
            "attachments": [
                {
                    "mrkdwn_in": ["text"],
                    "color": "warning",
                    "author_name": "Home Automation Bot",
                    "fields": [],
                    "footer": "home automation app"
                }
            ]
        }

    
    def reset_time_window(self):
        self.time_window_total_motion = 0
        self.time_window_limit = None

    def motion_detected(self):
        if not self.time_window_limit:
            self.time_window_limit = datetime.now() + timedelta(0, self.time_window_seconds)

            logging.info("--- Window Started ---")

        if datetime.now() < self.time_window_limit:
            logging.info("Motion detected")
            self.time_window_total_motion = self.time_window_total_motion + 1

            if self.time_window_total_motion >= self.time_window_motion_limit:
                logging.info("Somebody is home, turn on the lights")

                if not self.lights_on:
                    # setup slack message
                    message = { "value": "Parece que tem alguém em casa, vou acender a luz" }
                    self.slack_message["attachments"][0]["fields"].append(message)
                    
                    # send slack message and get message ts
                    slack_response = slack.send_message(custom_payload=json.dumps(self.slack_message))
                    self.slack_message["ts"] = slack_response.get("ts")

                    # self.voice_monkey.trigger_monkey("turn-on-office-lights")
                    self.lights_on = True

                    # setup the update of the initial slack message
                    self.slack_message["attachments"][0]["fields"][0]["value"] = "A luz foi acessa"
                    self.slack_message["attachments"][0]["color"] = "good"
                    
                    # send slack message
                    slack.update_message(custom_payload=json.dumps(self.slack_message))
                    
                    # reset slack message template
                    self.reset_slack_message_template()
                else:
                    logging.info("Lights already on")

                self.reset_time_window()
        else:
            logging.info("--- Window Closed ---")
            if self.time_window_total_motion < self.time_window_motion_limit:
                logging.info("Nobody is home, turning off the lights")

                if self.lights_on:
                    # setup slack message
                    message = { "value": "Parece que não tem ninguém em casa, vou apagar a luz" }
                    self.slack_message["attachments"][0]["fields"].append(message)
                    
                    # send slack message and get message ts
                    slack_response = slack.send_message(custom_payload=json.dumps(self.slack_message))
                    self.slack_message["ts"] = slack_response.get("ts")

                    # self.voice_monkey.trigger_monkey("turn-off-office-lights")
                    self.lights_on = False

                    # setup the update of the initial slack message
                    self.slack_message["attachments"][0]["fields"][0]["value"] = "A luz foi apagada"
                    self.slack_message["attachments"][0]["color"] = "good"
                    
                    # send slack message
                    slack.update_message(custom_payload=json.dumps(self.slack_message))
                    
                    # reset slack message template
                    self.reset_slack_message_template()
                else:
                    logging.info("Lights already off")

                self.reset_time_window()

        logging.info(
            f"{self.time_window_total_motion} motions detected in the window")
