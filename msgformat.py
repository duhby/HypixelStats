import random

#==============[SETTINGS]==============
announcement = "[aight]"
partyMax = 8
#======================================

# stops message from overlapping unintentionally
def insertNoBreak(msg):
    return msg.replace(" ","┈")

# adds invisible characters to prevent:
# - 'You cannot say the same message twice!'
def insertInvis(msg):
    for i in range(25):
        randomPos = random.randint(0,len(msg)-1)
        invischar = "⛬⛫⛭⛮⛶"
        msg = msg[:randomPos] + invischar[random.randint(0,4)] + msg[randomPos:]
    return msg

# splits party formatted messages into chunks
# to prevent going above the character limit
def chunks(l, n):
    for i in range(0, len(l), n):
        yield(l[i:i+n])

def spaces(msg,n):
    for i in range(n):
        msg = " " + msg
    return msg

def discordmsg():
    return "/w _stats +discord"

def discord_request(verifyCode):
    pack = []
    link = "Discord; https://discord.gg/g3PPN5Y - "
    pack.append(insertNoBreak(spaces("Your verification code is " + str(verifyCode),14)))
    pack.append(insertNoBreak("send the code in the verify channel within 2 minutes!"))
    return link + insertInvis(" ".join(pack))

def msg(raw):
    modeLabel = f"{raw['mode']}"
    pack = []
    pack.append("Made with <3 from FatDubs") # if you change this you suck and I will personally make sure you get banned from Hypixel Stats
    pack.append(discordmsg())
    pack.append(f"{modeLabel:-^51}")
    pack.append(insertNoBreak(raw["main"]))
    pack.append(f"{announcement:-^51}")
    return insertInvis(" ".join(pack))

def party(raws):
    blocks = chunks(raws,4)
    for block in blocks:
        pack = []
        pack.append("Made with <3 from FatDubs") # if you change this you suck and I will personally make sure you get banned from Hypixel Stats
        pack.append(f'[{modeDisplay[mode]}]')
        for line in block: pack.append(insertNoBreak(line))
        yield insertInvis(" ".join(pack))
    if announcement != "":
        yield(announcement)

def wrongSyntax():
    pack = []
    pack.append(discordmsg())
    pack.append(insertNoBreak("use '/msg _stats username' for overall stats"))
    pack.append(insertNoBreak("invite me to a party to check your teammates' stats"))
    pack.append("Get a full list of features by joining the discord above!")
    return insertInvis(" ".join(pack))

def party_too_large():
    pack = []
    pack.append(f"Max party size is {partyMax}!")
    return insertInvis(" ".join(pack))

def party_mode(mode):
    try: moden = int(mode[-1])
    except: pass

    if "oa" in mode:
        mode = "OVERALL"
    elif "bw" in mode:
        modeDisplay = ["OVERALL","SOLOS","DOUBLES","3v3v3v3","4v4v4v4"]
        mode = "BEDWARS " + modeDisplay[moden]
    elif "sw" in mode:
        modeDisplay = ["OVERALL","SOLO NORMAL","SOLO INSANE","TEAM NORMAL","TEAM INSANE","RANKED"]
        mode = "SW " + modeDisplay[moden]
    elif "duels" in mode:
        modeDisplay = ["OVERALL","SUMO","UHC","BRIDGE","CLASSIC"]
        mode = "DUELS " + modeDisplay[moden]
    elif "tkr" in mode:
        mode = "TURBO KART RACERS"
    elif "pit" in mode:
        mode = "PIT"

    return insertInvis(insertNoBreak(f"Got it! Next time you invite me I will show {mode} stats."))
