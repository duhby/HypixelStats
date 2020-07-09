from math import sqrt

def getLevel(exp):
    return sqrt(exp + 15312.5) - 125 / sqrt(2)) / (25*sqrt(2)

def getSwLevel(exp):
    xps = [0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
    if exp >= 15000:
        return (exp - 15000) / 10000. + 12
    else:
        for i in range(len(xps)):
            if exp < xps[i]:
                return i + float(exp - xps[i-1]) / (xps[i] - xps[i-1])

def int_to_Roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_num = ''
    i = 0
    while  num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

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
    mode = mode[-1]
    try: 
        data = player["stats"]["Bedwars"]
        level = player["achievements"]["bedwars_level"]
    except: 
        return None
    out = {}

    # overall
    if mode == "0":
        if "winstreak" in data:
            winstreak = data["winstreak"]
        else:
            winstreak = 0

        # messy ok leave me alone
        if "final_kills_bedwars" in data:
            finalkills = data["final_kills_bedwars"]
        else:
            finalkills = 0
        if "final_deaths_bedwars" in data:
            finaldeaths = data["final_deaths_bedwars"]
            fkdr = str(round(finalkills / finaldeaths,2))
        elif "final_kills_bedwars" in data:
            fkdr = finalkills
        else:
            fkdr = 0

        if "wins_bedwars" in data:
            wins = data["wins_bedwars"]
        else:
            wins = 0
        if "losses_bedwars" in data:
            losses = data["losses_bedwars"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "wins_bedwars" in data:
            wr = "100%"
        else:
            wr = "0%"

        if "beds_broken_bedwars" in data:
            bedsbroken = data["beds_broken_bedwars"]
        else:
            bedsbroken = 0
        if "beds_lost_bedwars" in data:
            bedslost = data["beds_lost_bedwars"]
            bblr = str(round(bedsbroken/(bedslost),1))
        elif "beds_broken_bedwars" in data:
            bblr = bedsbroken
        else:
            bblr = 0

    # solo
    if mode == "1":
        if "eight_one_winstreak" in data:
            winstreak = data["eight_one_winstreak"]
        else: winstreak = 0
        
        # messy ok leave me alone
        if "eight_one_final_kills_bedwars" in data:
            finalkills = data["eight_one_final_kills_bedwars"]
        else:
            finalkills = 0
        if "eight_one_final_deaths_bedwars" in data:
            finaldeaths = data["eight_one_final_deaths_bedwars"]
            fkdr = str(round(finalkills / finaldeaths,2))
        elif "eight_one_final_kills_bedwars" in data:
            fkdr = finalkills
        else:
            fkdr = 0

        if "eight_one_wins_bedwars" in data:
            wins = data["eight_one_wins_bedwars"]
        else:
            wins = 0
        if "eight_one_losses_bedwars" in data:
            losses = data["eight_one_losses_bedwars"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "eight_one_wins_bedwars" in data:
            wr = "100%"
        else:
            wr = "0%"

        if "eight_one_beds_broken_bedwars" in data:
            bedsbroken = data["eight_one_beds_broken_bedwars"]
        else:
            bedsbroken = 0
        if "eight_one_beds_lost_bedwars" in data:
            bedslost = data["eight_one_beds_lost_bedwars"]
            bblr = str(round(bedsbroken/(bedslost),1))
        elif "eight_one_beds_broken_bedwars" in data:
            bblr = bedsbroken
        else:
            bblr = 0

    # doubles
    if mode == "2":
        if "eight_two_winstreak" in data:
            winstreak = data["eight_two_winstreak"]
        else: winstreak = 0
        
        # messy ok leave me alone
        if "eight_two_final_kills_bedwars" in data:
            finalkills = data["eight_two_final_kills_bedwars"]
        else:
            finalkills = 0
        if "eight_two_final_deaths_bedwars" in data:
            finaldeaths = data["eight_two_final_deaths_bedwars"]
            fkdr = str(round(finalkills / finaldeaths,2))
        elif "eight_two_final_kills_bedwars" in data:
            fkdr = finalkills
        else:
            fkdr = 0

        if "eight_two_wins_bedwars" in data:
            wins = data["eight_two_wins_bedwars"]
        else:
            wins = 0
        if "eight_two_losses_bedwars" in data:
            losses = data["eight_two_losses_bedwars"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "eight_two_wins_bedwars" in data:
            wr = "100%"
        else:
            wr = "0%"

        if "eight_two_beds_broken_bedwars" in data:
            bedsbroken = data["eight_two_beds_broken_bedwars"]
        else:
            bedsbroken = 0
        if "eight_two_beds_lost_bedwars" in data:
            bedslost = data["eight_two_beds_lost_bedwars"]
            bblr = str(round(bedsbroken/(bedslost),1))
        elif "eight_two_beds_broken_bedwars" in data:
            bblr = bedsbroken
        else:
            bblr = 0

    # 3s
    if mode == "3":
        if "four_three_winstreak" in data:
            winstreak = data["four_three_winstreak"]
        else: winstreak = 0
        
        # messy ok leave me alone
        if "four_three_final_kills_bedwars" in data:
            finalkills = data["four_three_final_kills_bedwars"]
        else:
            finalkills = 0
        if "four_three_final_deaths_bedwars" in data:
            finaldeaths = data["four_three_final_deaths_bedwars"]
            fkdr = str(round(finalkills / finaldeaths,2))
        elif "four_three_final_kills_bedwars" in data:
            fkdr = finalkills
        else:
            fkdr = 0

        if "four_three_wins_bedwars" in data:
            wins = data["four_three_wins_bedwars"]
        else:
            wins = 0
        if "four_three_losses_bedwars" in data:
            losses = data["four_three_losses_bedwars"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "four_three_wins_bedwars" in data:
            wr = "100%"
        else:
            wr = "0%"

        if "four_three_beds_broken_bedwars" in data:
            bedsbroken = data["four_three_beds_broken_bedwars"]
        else:
            bedsbroken = 0
        if "four_three_beds_lost_bedwars" in data:
            bedslost = data["four_three_beds_lost_bedwars"]
            bblr = str(round(bedsbroken/(bedslost),1))
        elif "four_three_beds_broken_bedwars" in data:
            bblr = bedsbroken
        else:
            bblr = 0

    # 4s
    if mode == "4":
        if "four_four_winstreak" in data:
            winstreak = data["four_four_winstreak"]
        else: winstreak = 0
        
        # messy ok leave me alone
        if "four_four_final_kills_bedwars" in data:
            finalkills = data["four_four_final_kills_bedwars"]
        else:
            finalkills = 0
        if "four_four_final_deaths_bedwars" in data:
            finaldeaths = data["four_four_final_deaths_bedwars"]
            fkdr = str(round(finalkills / finaldeaths,2))
        elif "four_four_final_kills_bedwars" in data:
            fkdr = finalkills
        else:
            fkdr = 0

        if "four_four_wins_bedwars" in data:
            wins = data["four_four_wins_bedwars"]
        else:
            wins = 0
        if "four_four_losses_bedwars" in data:
            losses = data["four_four_losses_bedwars"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "four_four_wins_bedwars" in data:
            wr = "100%"
        else:
            wr = "0%"

        if "four_four_beds_broken_bedwars" in data:
            bedsbroken = data["four_four_beds_broken_bedwars"]
        else:
            bedsbroken = 0
        if "four_four_beds_lost_bedwars" in data:
            bedslost = data["four_four_beds_lost_bedwars"]
            bblr = str(round(bedsbroken/(bedslost),1))
        elif "four_four_beds_broken_bedwars" in data:
            bblr = bedsbroken
        else:
            bblr = 0

    # 4v4
    if mode == "5":
        if "two_four_winstreak" in data:
            winstreak = data["two_four_winstreak"]
        else: winstreak = 0
        
        # messy ok leave me alone
        if "two_four_final_kills_bedwars" in data:
            finalkills = data["two_four_final_kills_bedwars"]
        else:
            finalkills = 0
        if "two_four_final_deaths_bedwars" in data:
            finaldeaths = data["two_four_final_deaths_bedwars"]
            fkdr = str(round(finalkills / finaldeaths,2))
        elif "two_four_final_kills_bedwars" in data:
            fkdr = finalkills
        else:
            fkdr = 0

        if "two_four_wins_bedwars" in data:
            wins = data["two_four_wins_bedwars"]
        else:
            wins = 0
        if "two_four_losses_bedwars" in data:
            losses = data["two_four_losses_bedwars"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "two_four_wins_bedwars" in data:
            wr = "100%"
        else:
            wr = "0%"

        if "two_four_beds_broken_bedwars" in data:
            bedsbroken = data["two_four_beds_broken_bedwars"]
        else:
            bedsbroken = 0
        if "two_four_beds_lost_bedwars" in data:
            bedslost = data["two_four_beds_lost_bedwars"]
            bblr = str(round(bedsbroken/(bedslost),1))
        elif "two_four_beds_broken_bedwars" in data:
            bblr = bedsbroken
        else:
            bblr = 0

    out["level"] = level
    out["fkdr"] = fkdr
    out["wr"] = wr
    out["ws"] = winstreak
    out["bblr"] = bblr

    return out

def getSwStats(player,mode):
    mode = mode[-1]
    try: 
        data = player["stats"]["SkyWars"]
        level = round(getSwLevel(data["skywars_experience"]),1)
    except: 
        return None
    out = {}

    if "win_streak" in data:
        winstreak = data["win_streak"]
    else:
        winstreak = 0

    # overall
    if mode == "0":
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
        
        if "wins" in data:
            wins = data["wins"]
        else:
            wins = 0
        if "losses" in data:
            losses = data["losses"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "wins" in data:
            wr = "100%"
        else:
            wr = "0%"

    # solo normal
    if mode == "1":
        if "kills_solo_normal" in data:
            kills = data["kills_solo_normal"]
        else:
            kills = 0
        if "deaths_solo_normal" in data:
            deaths = data["deaths_solo_normal"]
            kd = str(round(kills / deaths,2))
        elif "kills_solo_normal" in data:
            kd = kills
        else:
            kd = 0
        
        if "wins_solo_normal" in data:
            wins = data["wins_solo_normal"]
        else:
            wins = 0
        if "losses_solo_normal" in data:
            losses = data["losses_solo_normal"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "wins_solo_normal" in data:
            wr = "100%"
        else:
            wr = "0%"

    # solo insane
    if mode == "2":
        if "kills_solo_insane" in data:
            kills = data["kills_solo_insane"]
        else:
            kills = 0
        if "deaths_solo_insane" in data:
            deaths = data["deaths_solo_insane"]
            kd = str(round(kills / deaths,2))
        elif "kills_solo_insane" in data:
            kd = kills
        else:
            kd = 0
        
        if "wins_solo_insane" in data:
            wins = data["wins_solo_insane"]
        else:
            wins = 0
        if "losses_solo_insane" in data:
            losses = data["losses_solo_insane"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "wins_solo_insane" in data:
            wr = "100%"
        else:
            wr = "0%"

    # team normal
    if mode == "3":
        if "kills_team_normal" in data:
            kills = data["kills_team_normal"]
        else:
            kills = 0
        if "deaths_team_normal" in data:
            deaths = data["deaths_team_normal"]
            kd = str(round(kills / deaths,2))
        elif "kills_team_normal" in data:
            kd = kills
        else:
            kd = 0
        
        if "wins_team_normal" in data:
            wins = data["wins_team_normal"]
        else:
            wins = 0
        if "losses_team_normal" in data:
            losses = data["losses_team_normal"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "wins_team_normal" in data:
            wr = "100%"
        else:
            wr = "0%"

    # team insane
    if mode == "4":
        if "kills_team_insane" in data:
            kills = data["kills_team_insane"]
        else:
            kills = 0
        if "deaths_team_insane" in data:
            deaths = data["deaths_team_insane"]
            kd = str(round(kills / deaths,2))
        elif "kills_team_insane" in data:
            kd = kills
        else:
            kd = 0
        
        if "wins_team_insane" in data:
            wins = data["wins_team_insane"]
        else:
            wins = 0
        if "losses_team_insane" in data:
            losses = data["losses_team_insane"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "wins_team_insane" in data:
            wr = "100%"
        else:
            wr = "0%"

    # ranked
    if mode == "5":
        if "kills_ranked" in data:
            kills = data["kills_ranked"]
        else:
            kills = 0
        if "deaths_ranked" in data:
            deaths = data["deaths_ranked"]
            kd = str(round(kills / deaths,2))
        elif "kills_ranked" in data:
            kd = kills
        else:
            kd = 0
        
        if "wins_ranked" in data:
            wins = data["wins_ranked"]
        else:
            wins = 0
        if "losses_ranked" in data:
            losses = data["losses_ranked"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "wins_ranked" in data:
            wr = "100%"
        else:
            wr = "0%"

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
    mode = mode[-1]
    try: data = player["stats"]["Duels"]
    except: return None
    out = {}

    # overall
    if mode == "0":       
        prestige = "Null"
        if "all_modes_rookie_title_prestige" in data:
            prestige = "Rookie " + int_to_Roman(data["all_modes_rookie_title_prestige"])
        if "all_modes_iron_title_prestige" in data:
            prestige = "Iron " + int_to_Roman(data["all_modes_iron_title_prestige"])
        if "all_modes_gold_title_prestige" in data:
            prestige = "Gold " + int_to_Roman(data["all_modes_gold_title_prestige"])
        if "all_modes_diamond_title_prestige" in data:
            prestige = "Diamond " + int_to_Roman(data["all_modes_diamond_title_prestige"])
        if "all_modes_master_title_prestige" in data:
            prestige = "Master " + int_to_Roman(data["all_modes_master_title_prestige"])
        if "all_modes_legend_title_prestige" in data:
            prestige = "Legend  " + int_to_Roman(data["all_modes_legend_title_prestige"])
        if "all_modes_grandmaster_title_prestige" in data:
            prestige = "GrandMaster " + int_to_Roman(data["all_modes_grandmaster_title_prestige"])
        if "all_modes_godlike_title_prestige" in data:
            prestige = "GodLike " + int_to_Roman(data["all_modes_godlike_title_prestige"])

        if "current_winstreak" in data:
            winstreak = data["current_winstreak"]
        else:
            winstreak = 0
        
        if "best_overall_winstreak" in data:
            bestws = data["best_overall_winstreak"]
        else:
            bestws = 0

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

        if "wins" in data:
            wins = data["wins"]
        else:
            wins = 0
        if "losses" in data:
            losses = data["losses"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "wins" in data:
            wr = "100%"
        else:
            wr = "0%"
        
    # sumo
    if mode == "1":
        prestige = "Null"
        if "sumo_rookie_title_prestige" in data:
            prestige = "Rookie " + int_to_Roman(data["sumo_rookie_title_prestige"])
        if "sumo_iron_title_prestige" in data:
            prestige = "Iron " + int_to_Roman(data["sumo_iron_title_prestige"])
        if "sumo_gold_title_prestige" in data:
            prestige = "Gold " + int_to_Roman(data["sumo_gold_title_prestige"])
        if "sumo_diamond_title_prestige" in data:
            prestige = "Diamond " + int_to_Roman(data["sumo_diamond_title_prestige"])
        if "sumo_master_title_prestige" in data:
            prestige = "Master " + int_to_Roman(data["sumo_master_title_prestige"])
        if "sumo_legend_title_prestige" in data:
            prestige = "Legend  " + int_to_Roman(data["sumo_legend_title_prestige"])
        if "sumo_grandmaster_title_prestige" in data:
            prestige = "GrandMaster " + int_to_Roman(data["sumo_grandmaster_title_prestige"])
        if "sumo_godlike_title_prestige" in data:
            prestige = "GodLike " + int_to_Roman(data["sumo_godlike_title_prestige"])

        if "current_sumo_winstreak" in data:
            winstreak = data["current_sumo_winstreak"]
        else:
            winstreak = 0
        
        if "best_sumo_winstreak" in data:
            bestws = data["best_sumo_winstreak"]
        else:
            bestws = 0

        if "sumo_duel_kills" in data:
            kills = data["sumo_duel_kills"]
        else:
            kills = 0
        if "sumo_duel_deaths" in data:
            deaths = data["sumo_duel_deaths"]
            kd = str(round(kills / deaths,2))
        elif "sumo_duel_kills" in data:
            kd = kills
        else:
            kd = 0

        if "sumo_duel_wins" in data:
            wins = data["sumo_duel_wins"]
        else:
            wins = 0
        if "sumo_duel_losses" in data:
            losses = data["sumo_duel_losses"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "sumo_duel_wins" in data:
            wr = "100%"
        else:
            wr = "0%"
    
    # uhc
    if mode == "2":
        prestige = "Null"
        if "uhc_rookie_title_prestige" in data:
            prestige = "Rookie " + int_to_Roman(data["uhc_rookie_title_prestige"])
        if "uhc_iron_title_prestige" in data:
            prestige = "Iron " + int_to_Roman(data["uhc_iron_title_prestige"])
        if "uhc_gold_title_prestige" in data:
            prestige = "Gold " + int_to_Roman(data["uhc_gold_title_prestige"])
        if "uhc_diamond_title_prestige" in data:
            prestige = "Diamond " + int_to_Roman(data["uhc_diamond_title_prestige"])
        if "uhc_master_title_prestige" in data:
            prestige = "Master " + int_to_Roman(data["uhc_master_title_prestige"])
        if "uhc_legend_title_prestige" in data:
            prestige = "Legend  " + int_to_Roman(data["uhc_legend_title_prestige"])
        if "uhc_grandmaster_title_prestige" in data:
            prestige = "GrandMaster " + int_to_Roman(data["uhc_grandmaster_title_prestige"])
        if "uhc_godlike_title_prestige" in data:
            prestige = "GodLike " + int_to_Roman(data["uhc_godlike_title_prestige"])

        if "current_uhc_winstreak" in data:
            winstreak = data["current_uhc_winstreak"]
        else:
            winstreak = 0
        
        if "best_uhc_winstreak" in data:
            bestws = data["best_uhc_winstreak"]
        else:
            bestws = 0

        if "uhc_duel_kills" in data:
            kills = data["uhc_duel_kills"]
        else:
            kills = 0
        if "uhc_duel_deaths" in data:
            deaths = data["uhc_duel_deaths"]
            kd = str(round(kills / deaths,2))
        elif "uhc_duel_kills" in data:
            kd = kills
        else:
            kd = 0

        if "uhc_duel_wins" in data:
            wins = data["uhc_duel_wins"]
        else:
            wins = 0
        if "uhc_duel_losses" in data:
            losses = data["uhc_duel_losses"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "uhc_duel_wins" in data:
            wr = "100%"
        else:
            wr = "0%"
    
    # bridge
    if mode == "3":
        prestige = "Null"
        if "bridge_rookie_title_prestige" in data:
            prestige = "Rookie " + int_to_Roman(data["bridge_rookie_title_prestige"])
        if "bridge_iron_title_prestige" in data:
            prestige = "Iron " + int_to_Roman(data["bridge_iron_title_prestige"])
        if "bridge_gold_title_prestige" in data:
            prestige = "Gold " + int_to_Roman(data["bridge_gold_title_prestige"])
        if "bridge_diamond_title_prestige" in data:
            prestige = "Diamond " + int_to_Roman(data["bridge_diamond_title_prestige"])
        if "bridge_master_title_prestige" in data:
            prestige = "Master " + int_to_Roman(data["bridge_master_title_prestige"])
        if "bridge_legend_title_prestige" in data:
            prestige = "Legend  " + int_to_Roman(data["bridge_legend_title_prestige"])
        if "bridge_grandmaster_title_prestige" in data:
            prestige = "GrandMaster " + int_to_Roman(data["bridge_grandmaster_title_prestige"])
        if "bridge_godlike_title_prestige" in data:
            prestige = "GodLike " + int_to_Roman(data["bridge_godlike_title_prestige"])

        if "current_bridge_winstreak" in data:
            winstreak = data["current_bridge_winstreak"]
        else:
            winstreak = 0
        
        if "best_bridge_winstreak" in data:
            bestws = data["best_bridge_winstreak"]
        else:
            bestws = 0

        if "bridge_duel_kills" in data:
            kills = data["bridge_duel_kills"]
        else:
            kills = 0
        if "bridge_duel_deaths" in data:
            deaths = data["bridge_duel_deaths"]
            kd = str(round(kills / deaths,2))
        elif "bridge_duel_kills" in data:
            kd = kills
        else:
            kd = 0

        if "bridge_duel_wins" in data:
            wins = data["bridge_duel_wins"]
        else:
            wins = 0
        if "bridge_duel_losses" in data:
            losses = data["bridge_duel_losses"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "bridge_duel_wins" in data:
            wr = "100%"
        else:
            wr = "0%"
    
    # classic
    if mode == "4":
        prestige = "Null"
        if "classic_rookie_title_prestige" in data:
            prestige = "Rookie " + int_to_Roman(data["classic_rookie_title_prestige"])
        if "classic_iron_title_prestige" in data:
            prestige = "Iron " + int_to_Roman(data["classic_iron_title_prestige"])
        if "classic_gold_title_prestige" in data:
            prestige = "Gold " + int_to_Roman(data["classic_gold_title_prestige"])
        if "classic_diamond_title_prestige" in data:
            prestige = "Diamond " + int_to_Roman(data["classic_diamond_title_prestige"])
        if "classic_master_title_prestige" in data:
            prestige = "Master " + int_to_Roman(data["classic_master_title_prestige"])
        if "classic_legend_title_prestige" in data:
            prestige = "Legend  " + int_to_Roman(data["classic_legend_title_prestige"])
        if "classic_grandmaster_title_prestige" in data:
            prestige = "GrandMaster " + int_to_Roman(data["classic_grandmaster_title_prestige"])
        if "classic_godlike_title_prestige" in data:
            prestige = "GodLike " + int_to_Roman(data["classic_godlike_title_prestige"])

        if "current_classic_winstreak" in data:
            winstreak = data["current_classic_winstreak"]
        else:
            winstreak = 0
        
        if "best_classic_winstreak" in data:
            bestws = data["best_classic_winstreak"]
        else:
            bestws = 0

        if "classic_duel_kills" in data:
            kills = data["classic_duel_kills"]
        else:
            kills = 0
        if "classic_duel_deaths" in data:
            deaths = data["classic_duel_deaths"]
            kd = str(round(kills / deaths,2))
        elif "classic_duel_kills" in data:
            kd = kills
        else:
            kd = 0

        if "classic_duel_wins" in data:
            wins = data["classic_duel_wins"]
        else:
            wins = 0
        if "classic_duel_losses" in data:
            losses = data["classic_duel_losses"]
            wr = str(round(wins/(losses+wins)*100))
            wr += "%"
        elif "classic_duel_wins" in data:
            wr = "100%"
        else:
            wr = "0%"

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
        prestige = int_to_Roman(player["achievements"]["pit_prestiges"])
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
