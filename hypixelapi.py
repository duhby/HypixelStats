import json
import requests
import getstats

#================[SETTINGS]================
keys = ["e973092a-e353-4842-a8cd-09e69ffbeefb",
        "d66d46a8-31a9-4f03-a470-65ed0498c06e"]

api_timeout = 5 # in seconds
#==========================================

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

def minimizeNumber(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

n = -1 # used to iterate through keys
def nextKey():
    global n
    n += 1
    return keys[n%len(keys)]

def getPlayer(username,mode):
    apikey = nextKey()
    try:
        response = requests.get(f"https://api.hypixel.net/player?key={apikey}&name={username}",timeout=api_timeout)
    except Exception:
        logging.info("API Timeout!")
        return {}
    try:
        player = response.json()
        if not player["success"]:
            logging.info("Key error: " + str(apikey))
            return {}

        player = player["player"]

        if player == None:
            player = {"displayname":username}

        if "displayname" in player:
            username = player["displayname"]

        out = {}
        out["username"] = player["displayname"]
        if "bw" in mode:
            out["stats"] = getstats.getBwStats(player,mode)
        elif "sw" in mode:
            out["stats"] = getstats.getSwStats(player,mode)
        elif "tkr" in mode:
            out["stats"] = getstats.getTkrStats(player)
        elif "duels" in mode:
            out["stats"] = getstats.getDuelStats(player,mode)
        elif "pit" in mode:
            out["stats"] = getstats.getPitStats(player)
        elif "oa" in mode:
            out["stats"] = getstats.getOverallStats(player)
        return out
    except Exception as error:
        logging.warning(error)
        return {}

def convert(data,mode):
    try:
        username = data["username"]
        stats = data["stats"]
        main = ""

        # can't put "if stats == None:" here bc mode needs to be the actual mode ik messy

        # overall
        if "oa" in mode:
            mode = "OVERALL"

            if stats == None:
                main = username + f" - Nicked? (No data) mode = {mode}"
            else:
                karma = minimizeNumber(stats["karma"])
                ap = minimizeNumber(stats["ap"])
                quests = minimizeNumber(stats["quests"])
                main = "[{:<6}]{:<12} Karma:{} AP:{} Quests:{}".format(stats["level"],username[:12],karma,ap,quests)

        # bedwars
        elif "bw" in mode:
            moden = int(mode[-1])
            modeDisplay = ["OVERALL","SOLOS","DOUBLES","3v3v3v3","4v4v4v4","4v4"]
            mode = "BW " + modeDisplay[moden]

            if stats == None:
                main = username + f" - Nicked? (No data) mode = {mode}"
            else:
                # messy...
                main = "[{:4d}✫]{:<12} FKDR:{} WR:{} WS:{} BBLR:{}".format(stats["level"],username[:12],stats["fkdr"],stats["wr"],stats["ws"],stats["bblr"])

        # skywars
        elif "sw" in mode:
            moden = int(mode[-1])
            modeDisplay = ["OVERALL","SOLO NORMAL","SOLO INSANE","TEAM NORMAL","TEAM INSANE","RANKED"]
            mode = "SW " + modeDisplay[moden]

            if stats == None:
                main = username + f" - Nicked? (No data) mode = {mode}"
            else:
                main = "[{:<3}✫]{:<16} KD:{} WS:{} WR:{}".format(stats["level"],username,stats["kd"],stats["ws"],stats["wr"])

        # gingerbread
        elif "tkr" in mode:
            mode = "TKR"

            if stats == None:
                main = username + f" - Nicked? (No data) mode = {mode}"
            else:
                main = "{:<16} Laps:{} G:{} S:{} B:{} BR:{}".format(username,minimizeNumber(stats["laps"]),minimizeNumber(stats["gold_trophies"]),minimizeNumber(stats["silver_trophies"]),minimizeNumber(stats["bronze_trophies"]),stats["banana_ratio"])

        # duels
        elif "duels" in mode:
            moden = int(mode[-1])
            modeDisplay = ["OVERALL","SUMO","UHC","BRIDGE","CLASSIC"]
            moden = int(mode[-1])
            mode = "DUELS " + modeDisplay[moden]

            if stats == None:
                main = username + f" - Nicked? (No data) mode = {mode}"
            else:
                main = "[{:<13}]{:12} KD:{} WS:{} BestWS:{} WR:{}".format(stats["prestige"],username[:12],stats["kd"],stats["ws"],stats["bestws"],stats["wr"])
            
        # pit
        elif "pit" in mode:
            mode = "PIT"

            if stats == None:
                main = username + f" - Nicked? (No data) mode = {mode}"
            else:
                main = "[{:<4}]{:12} KD:{} Highest KS:{}".format(stats["prestige"],username,stats["kd"],stats["max_streak"])

        return {"main":main,"mode":mode}

    except Exception as error:
        logging.error(error)
        return {"main":"Something went wrong!, please try again in a bit!","mode":"Null"}
