import time
import logging
from signal import pause
from gpiozero import MotionSensor
from dotenv import load_dotenv
from helpers.ifttt import trigger_webhook

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')
logging.getLogger('server.py')

lights_on = False

def motion_detected():
    # if not lights_on:
    #     logging.info("Turn the lights on")
    #     lights_on = True
    logging.info("Motion")
    # trigger_webhook("office_lights_on", "ciK5YTnqRD0Coe_ATf_zCd")

pir = MotionSensor(18)
pir.when_motion = motion_detected
pause()