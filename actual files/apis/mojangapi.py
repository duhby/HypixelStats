import requests
import json

api_timeout = 3 # in seconds

def getUUID(user):
    try:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}",timeout=api_timeout).json()
        return response["id"]
    except:
        logging.error("API Timeout! (mojang)")
        return None

def correctCaps(user):
    try:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}",timeout=api_timeout).json()
        return response["name"]
    except:
        logging.error("API Timeout! (mojang)")
        return user
