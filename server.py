import logging
from signal import pause
from gpiozero import MotionSensor
from dotenv import load_dotenv
from helpers.motion import MotionSense

load_dotenv()

motion_sense = MotionSense()

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')
logging.getLogger('server.py')

pir = MotionSensor(18)
pir.when_motion = motion_sense.motion_detected
pause()