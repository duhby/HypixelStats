# checks snipers using minutebrain and reza's api, more info on their discord
import requests
import json
import mojangapi

api_timeout = 3

# logging
from logging.handlers import TimedRotatingFileHandler # used for logging different files according to time
import logging # used for logging

# sets logging config to file and console
logging.basicConfig(
    level    = logging.INFO,
    format   = "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt  = '%I:%M:%S %p',
    handlers = [
        logging.StreamHandler(),
        logging.handlers.TimedRotatingFileHandler("logs/_stats.log", when = "midnight", interval = 1)
    ]
)

def isSniper(player):
    player = mojangapi.correctCaps(player)
    try:
        response = requests.get(f"http://161.35.53.44:8080/?playerv3={player}",timeout=api_timeout)
        text = response.text
        text = text.replace("\'","\"")
        text = text.lower()
        text = json.loads(text)
        return text
    except:
        logging.error("API Timeout! (minutebrain)")
    return False
