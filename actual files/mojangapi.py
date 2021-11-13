import requests
import json

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

api_timeout = 10 # in seconds

def getUUID(user):
    try:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{user}",timeout=api_timeout).json()
        if "id" in response:
            return response["id"]
        else:
            return None
    except:
        logging.error("API Timeout! (mojang)")
    
    return None

def correctCaps(user):
    try:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{user}",timeout=api_timeout).json()
        if "name" in response:
            return response["name"]
        else:
            return user
    except requests.exceptions.Timeout:
        logging.error("API Timeout! (mojang)")
    
    return user
