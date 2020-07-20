import random

#==============[SETTINGS]==============
announcement = ""
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

def msg(raw):
    modeLabel = f"[{raw['mode']}]"
    pack = []
    pack.append("Made with <3 from FatDubs") # Changing this is illegal and unethical so don't or there will be consequences.
    pack.append(insertNoBreak(discordmsg()))
    pack.append(f"{modeLabel:-^51}")
    pack.append(insertNoBreak(raw["main"]))
    pack.append(f"{announcement:-^51}")
    return insertInvis(" ".join(pack))

def party(raws,mode):
    blocks = chunks(raws,3)
    mode = displaymode(mode)
    yield f"Made with <3 from FatDubs" # Changing this is illegal and unethical so don't or there will be consequences.
    if random.randint(0,1) == 1:
        yield discordmsg()
    # yield f"[{mode}]"
    i = 0
    for block in blocks:
        i += 1
        pack = []
        if i == 1:
            pack.append(f"[{mode}]")
        else:
            pack.append("                  ")
        for line in block: pack.append(insertNoBreak(line))
        yield insertInvis(" ".join(pack))
    if announcement != "":
        yield announcement

def sniper(data,player):
    sniper = data["sniper"]
    reports = data["report"]
    label = f"[{player}]"
    sniper = data["sniper"]
    reports = data["report"]
    pack = []
    pack.append("Made with <3 from FatDubs") # Changing this is illegal and unethical so don't or there will be consequences.
    pack.append(f"{label:-^51}")
    pack.append(insertNoBreak(f"Is sniper: {sniper}     Reports: {reports}"))
    pack.append(f"{announcement:-^51}")
    return insertInvis(" ".join(pack))

def party_too_large():
    pack = []
    pack.append(f"Max party size is {partyMax}!")
    return insertInvis(" ".join(pack))

def discordmsg():
    discmsgs = ["'/w _stats +discord' for a full list of features!","'/w _stats +discord' for feature requests!      ","'/w _stats +discord' for an uptime viewer!    ","'/w _stats +discord' for a TODO list!                      "]
    return random.choice(discmsgs)

def discord_request():
    link = "Discord; https://discord.gg/PtsBc4b                "
    pack = []
    pack.append(insertNoBreak("Type !verify {username} in the #verify channel"))
    return link + insertInvis(" ".join(pack))

def wrong_syntax():
    pack = []
    pack.append(discordmsg())
    pack.append(insertNoBreak("use '/msg _stats username' for overall stats"))
    pack.append(insertNoBreak("invite me to a party to check your teammates' stats"))
    pack.append("Get a full list of features by joining the discord above!")
    return insertInvis(" ".join(pack))

def reset_modes():
    return insertInvis("Got it! Your settings are now reset to default.")

def msg_mode(mode):
    mode = displaymode(mode)

    if mode == "":
        return invalidmode()

    return insertInvis(f"Got it! Next time you message me without defining a mode, I will show {mode} stats.")

def party_mode(mode):
    mode = displaymode(mode)

    if mode == "":
        return invalidmode()

    return insertInvis(f"Got it! Next time you invite me I will show {mode} stats.")

def invalidmode():
    return insertInvis("Please enter a valid mode. More information on my discord. '/w _stats +discord'")

# converts code into display (ex. duels1 --> DUELS SUMO)
def displaymode(mode):
    try:
        moden = int(mode[-1])
    except: pass

    if "oa" in mode:
        mode = "OVERALL"
    elif "bw" in mode:
        modeDisplay = ["OVERALL","SOLOS","DOUBLES","3v3v3v3","4v4v4v4","4v4"]
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

    return mode
