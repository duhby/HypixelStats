# checks snipers using minutebrain and reza's api, more info on their discord
import requests
import json

api_timeout = 3

# logging
from logging.handlers import TimedRotatingFileHandler # used for logging different files according to time
import logging # used for logging

# sets logging config to file and console
logging.basicConfig(
    level    = logging.INFO,
    format   = "%(asctime)s [%(levelname)s] %(message)s",
    datefmt  = '%m/%d/%Y %I:%M:%S %p',
    handlers = [
        logging.StreamHandler(),
        logging.handlers.TimedRotatingFileHandler("logs/_stats.log", when = "midnight", interval = 1)
    ]
)

def isSniper(player):
    try:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}",timeout=api_timeout)
        response = json.loads(response.text)
        player = response["name"]
    except:
        print("API Timeout! (mojang)")
    try:
        response = requests.get(f"http://161.35.53.44:8080/?playerv3={player}",timeout=api_timeout)
        text = response.text
        text = text.replace("\'","\"")
        text = text.lower()
        text = json.loads(text)
        return text
    except:
        print("API Timeout! (minutebrain)")
    return False