from math import sqrt

def getLevel(exp):
    return (sqrt(exp + 15312.5) - 125 / sqrt(2)) / (25*sqrt(2))

# credit to MinuteBrain for converting php to python (idk php XD)
def getSwLevel(exp):
    level = 0
    for ezlv in [0,20,50,80,100,250,500,1000,1500,2500,4000,5000]:
        if exp-ezlv < 0: break
        exp -= ezlv
        level += 1
    return level + exp // 10000

def getRoman(n):
    val = [10, 9, 5, 4, 1]
    syb = ["X", "IX", "V", "IV", "I"]
    num = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            num += syb[i]
            n -= val[i]
        i += 1
    return num
        
def getOverallStats(player):
    try:
        exp = player["networkExp"]
        level = round(getLevel(exp),2)
        karma = player["karma"]
        ap = player["achievementPoints"]
        quests = player["achievements"]["general_quest_master"]
    except:
        return None
    
    out = {}
    out["level"] = level
    out["karma"] = karma
    out["ap"] = ap
    out["quests"] = quests
    return out

def getBwStats(player,mode):
    try:
        data = player["stats"]["Bedwars"]
        level = player["achievements"]["bedwars_level"]
    except:
        return None

    keys = ["winstreak","final_kills_bedwars","final_deaths_bedwars","wins_bedwars","losses_bedwars","beds_broken_bedwars","beds_lost_bedwars"]
    
    moders = ["eight_one_","eight_two_","four_three_","four_four_","two_four_"]

    moden = int(mode[-1])
    moden -= 1
    
    if moden != -1:
        for i in range(len(keys)):
            keys[i] = moders[moden] + keys[i]


    if keys[0] in data: 
        winstreak = data[keys[0]]
    else: 
        winstreak = 0
    
    # msg me on discord if you think I can make this less messy
    if keys[1] in data:
        finalkills = data[keys[1]]
    else:
        finalkills = 0
    if keys[2] in data:
        finaldeaths = data[keys[2]]
        fkdr = str(round(finalkills / finaldeaths,2))
    elif keys[1] in data:
        fkdr = finalkills
    else:
        fkdr = 0
    
    if keys[3] in data:
        wins = data[keys[3]]
    else:
        wins = 0
    if keys[4] in data:
        losses = data[keys[4]]
        wr = str(round(wins/(losses+wins)*100))
        wr += "%"
    elif keys[3] in data:
        wr = "100%"
    else:
        wr = "0%"
    
    if keys[5] in data:
        bedsbroken = data[keys[5]]
    else:
        bedsbroken = 0
    if keys[6] in data:
        bedslost = data[keys[6]]
        bblr = str(round(bedsbroken/bedslost,1))
    elif keys[5] in data:
        bblr = bedsbroken
    else:
        bblr = "0"
    
    out = {}
    out["level"] = level
    out["fkdr"] = fkdr
    out["wr"] = wr
    out["ws"] = winstreak
    out["bblr"] = bblr

    return out

def getSwStats(player,mode):
    try:
        data = player["stats"]["SkyWars"]
        level = round(getSwLevel(data["skywars_experience"]),1)
    except:
        return None

    # the only winstreak data in the api is overall
    if "win_streak" in data:
        winstreak = data["win_streak"]
    else:
        winstreak = 0
    
    keys = ["kills","deaths","wins","losses"]
    moders = ["_solo_normal","_solo_insane","_teams_normal","_teams_insane","_ranked"]

    moden = int(mode[-1])
    moden -= 1
    
    if moden != -1:
        for i in range(len(keys)):
            keys[i] += moders[moden]

    if keys[0] in data:
        kills = data[keys[0]]
    else:
        kills = 0
    if keys[1] in data:
        deaths = data[keys[1]]
        kd = str(round(kills / deaths,2))
    elif keys[0] in data:
        kd = kills
    else:
        kd = 0
    
    if keys[2] in data:
        wins = data[keys[2]]
    else:
        wins = 0
    if keys[3] in data:
        losses = data[keys[3]]
        wr = str(round(wins/(losses+wins)*100))
        wr += "%"
    elif keys[3] in data:
        wr = "100%"
    else:
        wr = "0%"

    out = {}
    out["level"] = level
    out["kd"] = kd
    out["wr"] = wr
    out["ws"] = winstreak

    return out

def getTkrStats(player):
    try: data = player["stats"]["GingerBread"]
    except: return None
    out = {}

    if "laps_completed" in data:
        laps = data["laps_completed"]
    else:
        laps = 0

    # if "wins" in data:
    #     wins = data["wins"]
    # else:
    #     wins = 0

    if "gold_trophy" in data:
        gold = data["gold_trophy"]
    else:
        gold = 0

    if "silver_trophy" in data:
        silver = data["silver_trophy"]
    else:
        silver = 0

    if "bronze_trophy" in data:
        bronze = data["bronze_trophy"]
    else:
        bronze = 0

    # if "box_pickups" in data:
    #     boxes = data["box_pickups"]
    # else:
    #     boxes = 0

    if "banana_hits_sent" in data:
        sent = data["banana_hits_sent"]
    else:
        sent = 0
    if "banana_hits_received" in data:
        received = data["banana_hits_received"]
        br = str(round(sent / received,2))
    elif "banana_hits_sent" in data:
        br = sent
    else:
        br = 0

    out["laps"] = laps
    # out["wins"] = wins
    out["gold_trophies"] = gold
    out["silver_trophies"] = silver
    out["bronze_trophies"] = bronze
    # out["powerups"] = boxes
    out["banana_ratio"] = br

    return out

def getDuelStats(player,mode):
    moden = int(mode[-1])
    try: data = player["stats"]["Duels"]
    except: return None
    
    titlekeys = ["all_modes_","sumo_","uhc_","bridge_","classic_"]
    titletxt = ["rookie_title_prestige","iron_title_prestige","gold_title_prestige","diamond_title_prestige","master_title_prestige","legend_title_prestige","grandmaster_title_prestige","godlike_title_prestige"]
    titles = ["Rookie ","Iron ","Gold ","Diamond ","Master ","Legend ","GrandMaster ","GodLike "]

    for i in range(len(titletxt)):
        titletxt[i] = titlekeys[moden] + titletxt[i]
    
    for i in range(len(titletxt)):
        prestige = titles[i] + getRoman(data[titletxt[i]])
    
    keys = ["kills","deaths","wins","losses"]
    moders = ["sumo_duel_","uhc_duel_","bridge_duel_","classic_duel_"]

    for i in range(len(keys)):
        keys[i] = moders[moden] + keys[i]

    # :/
    if moden == 0:
        best = "best_overall_winstreak"
        current = "current_winstreak"
    elif moden == 1:
        best = "best_sumo_winstreak"
        current = "current_sumo_winstreak"
    elif moden == 2:
        best = "best_uhc_winstreak"
        current = "current_uhc_winstreak"
    elif moden == 3:
        best = "best_bridge_winstreak"
        current = "current_bridge_winstreak"
    elif moden == 4:
        best = "best_classic_winstreak"
        current = "current_classic_winstreak"
    
    if current in data:
        winstreak = data[current]
    else:
        winstreak = 0
    
    if best in data:
        bestws = data[best]
    else:
        bestws = 0
    
    if keys[0] in data:
        kills = data[keys[0]]
    else:
        kills = 0
    if keys[1] in data:
        deaths = data[keys[1]]
        kd = str(round(kills / deaths,2))
    elif keys[0] in data:
        kd = kills
    else:
        kd = 0

    if keys[2] in data:
        wins = data[keys[2]]
    else:
        wins = 0
    if keys[3] in data:
        losses = data[keys[3]]
        wr = str(round(wins/(losses+wins)*100))
        wr += "%"
    elif keys[2] in data:
        wr = "100%"
    else:
        wr = "0%"

    out = {}
    out["prestige"] = prestige
    out["kd"] = kd
    out["ws"] = winstreak
    out["bestws"] = bestws
    out["wr"] = wr

    return out

def getPitStats(player):
    try: data = player["stats"]["Pit"]["pit_stats_ptl"]
    except: return None
    out = {}

    if "pit_prestiges" in player["achievements"]:
        prestige = roman(player["achievements"]["pit_prestiges"])
    else:
        prestige = "None"

    if "kills" in data:
        kills = data["kills"]
    else:
        kills = 0
    if "deaths" in data:
        deaths = data["deaths"]
        kd = str(round(kills / deaths,2))
    elif "kills" in data:
        kd = kills
    else:
        kd = 0

    if "max_streak" in data:
        highest_streak = data["max_streak"]
    else:
        highest_streak = 0

    out["prestige"] = prestige
    out["kd"] = kd
    out["max_streak"] = highest_streak

    return out
