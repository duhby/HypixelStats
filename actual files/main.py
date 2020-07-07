# Main project file

# files
import hypixelapi # grabs data from the hypixel api
import minuteapi # grabs data from minutebrain and reza's sniper api
import msgformat # self explanatory

# PyCraft imports for minecraft related processes
from minecraft import authentication as auth
from minecraft.exceptions import YggdrasilError # login error
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound
from minecraft.compat import input

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
        logging.handlers.TimedRotatingFileHandler("logs/bot.log", when = "midnight", interval = 1)
    ]
)

# other
from threading import Thread # speeds up i/o bound getStats functions
import time    # used for cooldown
import pickle  # used to write and read files
import sys     # used for the sys.exit() function
import json    # used to grab chat data from packets
import random  # used to randomize heartbeat messages

# class for utilities that are used frequently
# and would be messy if used in the main class
class utils:
    # converts the json data into a raw message
    def msg_raw(msg_json):
        try:
            msg = ""
            if "text" in msg_json:
                msg += msg_json["text"]
            if "extra" in msg_json:
                for i in msg_json["extra"]:
                    if "text" in i:
                        msg += i["text"]
            return(msg)
        except Exception as error:
            logging.warning(error)

    # removes invisible characters from message
    def removeInvis(msg):
        return("".join(x for x in msg if x not in "-⛬⛫⛭⛮⛶_"))

    def index(msg,index):
        return msg[msg.index("Your mute will expire in")+index:]

    def clean_msg(msg):
        valid_chars = "abcdefghijklmnopqrstuvwxyz_ :[]+/1234567890"
        valid_chars_send = "abcdefghijklmnopqrstuvwxyz_ :[]+/1!2@3#4$5%6^7&8*9(0)-=+" # if +send in msg use '`' and '~' to spam
        if "+send" not in msg.lower():
            msg = "".join(i for i in msg if i.lower() in valid_chars) # removes spam characters from message
        else:
            msg = "".join(i for i in msg if i.lower() in valid_chars_send) # removes ` and ~ from msg (and other nonvalid characters)
        msg = " ".join(msg.split()) # removes double space
        msg = msg.replace("+ ","+").replace("++","+").replace("+]","]")
        return msg
    
    # used for combining dictionaries for quota and verified users
    def combine_dict(one,two):
        for key in list(two):
            utils.increment_dict(one,key,two[key])

    def increment_dict(dic,key,n):
        if key in dic:    dic[key] += n
        else:             dic[key]  = n

    # saves a pkl file
    def save_obj(obj, name):
        with open('obj/'+ name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    # loads a pkl file
    def load_obj(name):
        with open('obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    class multithreading:
        def __init__(self,users,mode):
            self.userlist = users
            self.output = {}
            self.mode = mode
        def getplayerdata(self,user,mode):
            global output
            data = hypixelapi.getPlayer(user,mode)
            text = hypixelapi.convert(data,mode)["main"]
            self.output[user] = text
        def start(self):
            self.threads = []
            for user in self.userlist: self.threads.append(Thread(target=self.getplayerdata, args=(user,self.mode)))
            for thread in self.threads: thread.start()
            for thread in self.threads: thread.join()

# main class for the bot and it's functions
class bot:
    def __init__(self,email,password,username,rate):
        # define authentication objects
        self.email = email
        self.password = password
        self.username = username
        self.rate = rate
        self.auth_token = auth.AuthenticationToken()

        # validates credentials and connects to hypixel
        try: self.auth_token.authenticate(self.email,self.password)
        except YggdrasilError as error: 
            logging.warning(error)
            sys.exit()
        logging.info(f'Logged in as {self.email}.')
        self.connection = Connection('mc.hypixel.net',25565,auth_token=self.auth_token)

        # define objects
        self.msgQueue = []      # holds the queue for messages to send
        self.partyQueue = []    # holds the queue for parties to accept
        self.commandQueue = []  # holds the queue for commands to send
        self.command_delay = 0  # prevents sending commands too fast
        self.inParty = {"in":False,"from":"","timestamp":0}
        self.party_config = {}     # holds the data for players' party settings when they do +pmode
        self.player_cooldown = {}  # holds the cooldown time for players
        self.cooldown_timer = time.time()  # starts the cooldown timer
        self.heartbeat = time.time()       # starts the heartbeat timer
        self.heartbeat_cooldown = time.time()  # makes sure the bot doesn't send multiple messages to itself (due to lag)
        self.muted = False       # returns a boolean if the bot is muted
        self.mute_duration = 0   # holds the mute duration of the bot
        self.unmute_time = 0     # holds a timer until a bot is muted according to time.time()
        self.current_load = 0    # holds the current load data
        self.inQueue = False     # returns a boolean if the bot is in queue
        self.leader_buffer = ""  # holds the buffer for the leader of the party
        self.mods_buffer = []    # holds the buffer for the moderators of the party
        self.ops = ["FatDubs","gamerboy80"]  # holds the data for operators of the bot (case sensitive)
        self.quota = utils.load_obj("quota") # holds the amount of unique users and requests each user has
        self.quotaChange = {} # temporarily holds quota data to get added to self.quota during a hb
        topusers = {k: v for k, v in sorted(self.quota.items(), key=lambda item: item[1], reverse=True)}
        topusers = utils.clean_msg(str(topusers))
        topusers = topusers.split(" ")
        topusers = topusers[:6] # displays 3 users
        topusers = utils.clean_msg(str(topusers))

        logging.info(f"Unique users - {len(self.quota)}")
        logging.info(f"Total requests - {sum(self.quota.values())}")
        logging.info(f"Top users -\n{topusers}")

    # disconnects from the server
    def disconnect(self):
        self.msgQueue = []
        self.partyQueue = []
        self.connection.disconnect(True)
        sys.exit()

    # connects to the server using packets and stuff idk
    def initialize(self):
        self.connection.register_packet_listener(self.handle_join_game, clientbound.play.JoinGamePacket)
        self.connection.register_packet_listener(self.handle_chat, clientbound.play.ChatMessagePacket)
        self.connection.connect()

    # handles heartbeat and party on game join
    def handle_join_game(self,packet):
        time.sleep(0.5)
        self.chat("/p leave")
        logging.info('Connected.')

    def limbo(self):
        logging.info("Warp to Limbo")
        self.chat(chr(167))
        self.chat("/whereami")

    # sends a chat packet to the server
    def chat(self,text,delay=0.7,bypass=False):
        if not self.inQueue or bypass: # prevents sending messages while in queue (other than messages to get out of queue)
            text = text[:255] # limits to 255 characters
            packet = serverbound.play.ChatPacket()
            packet.message = text
            self.connection.write_packet(packet)
        self.command_delay = time.time()
        time.sleep(delay)

    def chat_party(self,msg,delay=0.5):
        while len(self.msgQueue) > 0:
            self.msg_tick()
            time.sleep(0.05)
        while time.time()-self.command_delay < delay: time.sleep(0.05)
        self.chat(msg,delay)
        self.inParty["timestamp"] = time.time()

    def handle_chat(self,chat_packet):
        try:
            chat_raw = str(chat_packet.json_data)
            chat_json = json.loads(str(chat_packet.json_data))
            msg = utils.msg_raw(chat_json)
            logging.debug(chat_raw)
            logging.debug(msg)
            length = len(msg)
            if not self.muted:
                if "red" in chat_raw and length < 75 and "+]" not in msg:
                    mutedetect = utils.removeInvis(msg) # removes invisible characters from message (necessary?)
                    if "Your mute will expire in" in mutedetect:
                        self.muted = True
                        duration = utils.index(mutedetect,24)
                        duration = duration.split()
                        duration = [x.strip() for x in duration if x.strip()[-1] in "dhms"] # removes d h m and s from muted message
                        mute = 0
                        for i in duration:
                            try:
                                duration = {"d":86400,"h":3600,"m":60,"s":1}
                                mute += duration[i[-1]] * int(i[:-1])
                            except Exception:
                                pass
                        self.unmute_time = time.time() + self.mute_duration
                        self.limbo()

                # if there is more than one format of chat on a single line
                if "extra" in chat_json:
                    logging.debug(msg)
                    # on party request
                    if "/party accept" in chat_raw:
                        # retreives the user that sent the invitation
                        for data in chat_json["extra"]:
                            if "/party accept" in str(data):
                                user = data["clickEvent"]["value"].split()[-1]
                                if self.cooldowncheck(user,5) and user not in self.ops: return # if user has cooldown level of 6 or more
                                self.partyQueue.append({"mode":"queue","user":user})
                                return
                        return

                    # on heartbeat
                    elif "HeartBeat-KeepAlive" in chat_raw and "from" not in chat_raw.lower() and self.username in chat_raw:
                        self.heartbeat = time.time()
                        return

                    # on party leader return
                    elif "Party Leader" in chat_raw and "●" in chat_raw:
                        # msg = Party Leader: [MVP+] FatDubs ●
                        leader = msg[msg.index(":")+1:].split("●") # retreive player
                        leader = leader[0].split()[-1] # remove rank
                        self.leader_buffer = leader
                        self.mods_buffer = []
                        # leader = 'FatDubs'

                    # on party moderator list return
                    elif "Party Moderators" in chat_raw and "●" in chat_raw:
                        # Party Moderators: [MVP++] Sneaak ● [YOUTUBE] gamerboy80 ●
                        mods = [mods for mods in msg[msg.index(":")+1:].split("●") if len(mods)>1] # if statement removes "list out of range" error
                        mods = [mods.split()[-1] for mods in mods] # removes ranks
                        self.mods_buffer = mods
                        # mods = ['Sneaak', 'gamerboy80']

                    elif "Party Members" in chat_raw and "●" in chat_raw:
                        # Party Members: [VIP] MinuteBrain ● hystats_ ●
                        users = [user for user in msg[msg.index(":")+1:].split("●") if len(user)>1] # if statement removes "list out of range" error
                        users = [user.split()[-1] for user in users] # removes ranks
                        users.remove(self.username) # removes bot from the list
                        users.append(self.leader_buffer)
                        users.extend(self.mods_buffer)
                        self.partyQueue = [{"mode":"list","user":users}] + self.partyQueue # puts ontop of the queue
                        return

                    # on msg request
                    elif ("From" in chat_raw) and ("light_purple" in chat_raw) and (self.username not in chat_raw):
                        self.chat_msg(msg)
                        return

                    # on friend request
                    elif ("Click to" in chat_raw) and ("/f accept " in chat_raw):
                        for data in chat_json["extra"]:
                            if "/f accept " in str(data).lower():
                                user = data["clickEvent"]["value"].split()[-1]
                                if self.cooldowncheck(user,2) and user not in self.ops: return
                                self.commandQueue.append({"command":"friend_request","user":user})
                                return
                        return

                    # on queue
                    elif ("The games starts in" in chat_raw) or ("has joined" in msg and "/" in msg) or ("has quit" in msg and "/" in msg) or ("Party Leader," in chat_raw and "yellow" in chat_raw):
                        if not self.inQueue:
                            self.inQueue = True
                            logging.info(str(self.inParty["from"]) + "summoned you to their server")
                            self.cooldowncheck(self.inParty["from"],60) # adds them to the blacklist for 6 minutes
                            self.inParty["in"] = True
                            self.inParty["timestamp"] = time.time()+9999
                            self.chat("/p leave",1,True)
                            self.chat("/l",0.7,True)
                            self.limbo()
                            self.inParty["in"] = False
                            self.inParty["timestamp"] = time.time()+5
                            self.inQueue = False
                        return

                    # on whereami respond
                    elif "You are currently" in msg and "aqua" in chat_raw:
                        logging.info(msg)
                        if "limbo" not in msg:
                            self.limbo()

            # while muted
            else:
                self.botsChange += {self.username:{"muted":True,"load":0}}
        except Exception as error:
            logging.warning("Chat handle error! " + str(error))

    def chat_msg(self,msg):
        # >>> msg = 'From [MVP+] FatDubs: FatDubs gamerboy80 tkr'
        msg = utils.clean_msg(msg)
        user = msg[:msg.index(":")].split()[-1]
        extra = msg[msg.index(":")+1:].split()
        extra = [i.lower() for i in extra] # converts list to lowercase

        # user = 'FatDubs'
        # extra = ['fatdubs', 'gamerboy80', 'tkr']

        mode = "oa"

        if len(extra)>1 and "+send" not in extra:
            # bedwars stats request
            #any(item in foo for item in bar)
            if any(item in extra[-2:] for item in ["bw","bedwars"]):
                mode = "bw"
                try: extra.remove("bw")
                except: pass
                try: extra.remove("bedwars")
                except: pass
                modifier = 0
                if extra[-1] in [str(x) for x in range(6)]:
                    modifier = str(extra.pop(-1))
                mode += str(modifier)
            # skywars stats request
            elif any(item in extra[-2:] for item in ["sw","skywars"]):
                mode = "sw"
                try: extra.remove("sw")
                except: pass
                try: extra.remove("skywars")
                except: pass
                modifier = 0
                if extra[-1] in [str(x) for x in range(6)]:
                    modifier = str(extra.pop(-1))
                mode += str(modifier)

            # duels stats requests
            elif "duels" in extra[-2:]:
                mode = "duels"
                extra.remove("duels")
                modifier = 0
                if "sumo" in extra[-1] or "1" in extra[-1]:
                    modifier = 1
                    try: extra.remove('sumo')
                    except: pass
                    try: extra.remove('1')
                    except: pass
                # uhc duels stats request
                elif "uhc" in extra[-1] or "2" in extra[-1]:
                    modifier = 2
                    try: extra.remove('uhc')
                    except: pass
                    try: extra.remove('2')
                    except: pass
                # bridge duels stats request
                elif "bridge" in extra[-1] or "3" in extra[-1]:
                    modifier = 3
                    try: extra.remove('bridge')
                    except: pass
                    try: extra.remove('3')
                    except: pass
                # classic duels stats request
                elif "classic" in extra[-1] or "4" in extra[-1]:
                    modifier = 4
                    try: extra.remove('classic')
                    except: pass
                    try: extra.remove('4')
                    except: pass
                mode += str(modifier)

            # tkr stats request
            elif "tkr" in extra[-1] or "gingerbread" in extra[-1]:
                mode = "tkr"
                del extra[-1]
            # the pit stats request
            elif "pit" in extra[-1:]:
                mode = "pit"
                del extra[-1]
            elif "overall" in extra[-1]:
                mode = "oa"
                del extra[-1]

        # user = 'FatDubs'
        # extra = ['fatdubs', 'gamerboy80']
        # mode = 'tkr'

        if self.cooldowncheck(user,1) and user not in self.ops: return # cooldown

        # commands
        if "+" in msg:
            cmd = extra[0]
            length = len(extra)
            if cmd == "+send" and user in self.ops:
                self.commandQueue.append({"command":"send_command","send":" ".join(extra[1:])})

            elif cmd in ["+c","+check"] and length == 2:
                data = minuteapi.isSniper(extra[-1])
                self.msgQueue = [{"msgMode":"sniper","user":user,"player":extra[-1],"data":data}] + self.msgQueue

            elif cmd in ["+pmode","+setpartymode"]:
                self.party_config[user] = mode
                self.msgQueue = [{"msgMode":"party_mode","user":user,"mode":mode}] + self.msgQueue
            
            elif cmd == "+discord":
                self.msgQueue = [{"msgMode":"discord_request","user":user}]

            else:
                self.msgQueue = [{"msgMode":"wrong_syntax","user":user}] + self.msgQueue

            return

        # stats request
        if len(extra) > 0 and len(extra[0]) < 17:
            if len(extra) == 1:
                self.msgQueue = [{"msgMode":"stats","replyto":user, "username":extra[0], "mode":mode}] + self.msgQueue
            # elif len(extra) > 1 and len(extra) < 6:
            #     self.msgQueue = [{"msgMode":"stats_multiple", "replyto":user, "username":extra, "mode":mode}] + self.msgQueue
            else:
                self.msgQueue = [{"msgMode":"wrong_syntax", "user":user}] + self.msgQueue
        else:
            self.msgQueue = [{"msgMode":"wrong_syntax", "user":user}] + self.msgQueue

    # returns True if a player has over 6 cooldown
    def cooldowncheck(self,user,n=1):
        if user not in self.player_cooldown: # adds the user to the cooldown list at level n
            self.player_cooldown[user] = n
        else:
            self.player_cooldown[user] += n # adds n to the user's initial cooldown

        if self.player_cooldown[user] > 6 and user not in self.ops:
            logging.warning(f"Reject spam from '{user}' level - {self.player_cooldown[user]}")
            return True # rejects spam from the user and stops the code that requested the cooldowncheck
        else:
            self.current_load += 1
            return False # continues with rest of code

    def cooldown_tick(self):
        if time.time()-self.cooldown_timer >= 6:
            self.cooldown_timer = time.time()
            for user in list(self.player_cooldown):
                self.player_cooldown[user] -= 1
            self.player_cooldown = {x:self.player_cooldown[x] for x in list(self.player_cooldown) if self.player_cooldown[x] > 0}

    def msg_tick(self):
        if len(self.msgQueue) > 0:
            currentQueue = self.msgQueue.pop(0)
            if currentQueue["msgMode"] == "stats":
                while time.time()-self.command_delay < 0.7: time.sleep(0.05)
                self.chat("/r",0)
                replyTo = currentQueue["replyto"]
                username = currentQueue["username"].lower()
                if currentQueue["username"] == "me":
                    username = replyTo
                mode = currentQueue["mode"]
                utils.increment_dict(self.quotaChange,replyTo,1)
                data = hypixelapi.getPlayer(username,mode)
                raw = hypixelapi.convert(data,mode)
                msg = msgformat.msg(raw)
                logging.info(f"{mode} Stats: {replyTo} --> {username}")
                self.chat(msg,0.4)

            ## NOT CURRENTLY SUPPORTED
            # elif currentQueue["msgMode"] == "stats_multiple":
                # while time.time()-self.command_delay < 0.6: time.sleep(0.05)
                # self.chat("/r",0)
                # replyTo = currentQueue["replyto"]
                # usernames = currentQueue["username"]
                # mode = currentQueue["mode"]
                # utils.increment_dict(self.quotaChange,replyTo,len(usernames))
                # output = {}
                # for user in usernames:
                #     data = hypixelapi.getPlayer(user,mode)
                #     text = hypixelapi.convert(data,mode)["main"]
                #     output[user] = text
                # raws = [output[x] for x in list(output)]
                # msgs = list(msgformat.party(raws,mode))
                # while time.time()-self.command_delay < 0.7: time.sleep(0.05)
                # for msg in msgs: self.chat(msg,0.4)

            elif currentQueue["msgMode"] == "discord_request":
                logging.info(f"Discord Request: {currentQueue['user']}")
                while time.time()-self.command_delay < 0.5: time.sleep(0.05)
                self.chat("/r " + msgformat.discord_request())

            # api by minutebrain and reza
            elif currentQueue["msgMode"] == "sniper":
                while time.time()-self.command_delay < 0.5: time.sleep(0.05)
                self.chat("/r",0)
                data = currentQueue["data"]
                player = currentQueue["player"]
                user = currentQueue["user"]
                utils.increment_dict(self.quotaChange,user,1)
                msg = msgformat.sniper(data,player)
                logging.info(f"Sniper Check: {user} --> {player}")
                self.chat(msg,0.4)

            elif currentQueue["msgMode"] == "wrong_syntax":
                logging.info(f"Wrong Syntax: {currentQueue['user']}")
                while time.time()-self.command_delay < 0.5: time.sleep(0.05)
                self.chat("/r " + msgformat.wrong_syntax(),0.5)
            
            elif currentQueue["msgMode"] == "party_mode":
                logging.info(f"Party Mode: {currentQueue['user']} --> {currentQueue['mode']}")
                while time.time()-self.command_delay < 0.5: time.sleep(0.05)
                self.chat("/r " + msgformat.party_mode(currentQueue["mode"]),0.5)
            
    def party_tick(self):
        if len(self.partyQueue) > 0 and len(self.msgQueue) == 0:
            currentQueue = self.partyQueue.pop(0)
            if currentQueue["mode"] == "queue" and self.inParty["in"]: # requeue if in party
                self.partyQueue.append(currentQueue)
            else:
                if currentQueue["mode"] == "queue":
                    self.inParty = {"in":True,"from":currentQueue["user"]}
                    logging.info(f"Party Accepted - {self.inParty['from']}")
                    utils.increment_dict(self.quotaChange,self.inParty["from"],1)
                    while time.time()-self.command_delay < 0.5: time.sleep(0.05)
                    self.chat_party(f"/p accept {self.inParty['from']}",0.4)
                    self.chat_party(f"/pl",0.3)
                elif currentQueue["mode"] == "list":
                    users = currentQueue["user"]
                    logging.info("Party List - " + " ".join(users))
                    if len(users) <= msgformat.partyMax:
                        if self.inParty["from"] in self.party_config:
                            mode = self.party_config[self.inParty["from"]]
                        else:
                            mode = "oa"
                        handle = utils.multithreading(users,mode)
                        handle.start()
                        raws = [handle.output[x] for x in list(handle.output)]
                        msgs = msgformat.party(raws,mode)
                        while time.time()-self.command_delay < 0.3: time.sleep(0.05)
                        for msg in msgs: self.chat_party(f"/pchat {msg}",0.3)
                    else:
                        while time.time()-self.command_delay < 0.3: time.sleep(0.05)
                        self.chat_party("/pchat " + msgformat.party_too_large(),0.3)
                    while time.time()-self.command_delay < 1:
                        self.msg_tick()
                        time.sleep(0.05)
                    self.chat("/p leave")
                    self.inParty["in"] = False
        if self.inParty["in"] and time.time()-self.inParty["timestamp"] > 2:
            logging.info("Party timeout!" + str(self.inParty["from"]))
            while time.time()-self.command_delay < 0.8: time.sleep(0.05)
            self.chat("/p leave",0.3)
            self.inParty["in"] = False
    
    def command_tick(self):
        if len(self.commandQueue) > 0:
            currentQueue = self.commandQueue.pop(0)

            if currentQueue["command"] == "friend_request":
                logging.info(f"Friend accepted - {currentQueue['user']}")
                while time.time()-self.command_delay < 0.7: time.sleep(0.05)
                self.chat(f"/f accept {currentQueue['user']}",0.3)
            
            elif currentQueue["command"] == "send_command":
                logging.info(f"Command sent - {currentQueue['send']}")
                while time.time()-self.command_delay < 0.7: time.sleep(0.05)
                self.chat(currentQueue["send"],0.3,True)
    
    def heartbeat_tick(self):
        if time.time()-self.heartbeat > 610:
            self.connection.disconnect(True)
            raise Exception("No heartbeat detect!")
            return
        
        if time.time()-self.heartbeat > 120:
            self.connection.connect()
            logging.info("Reconnecting..")
        
        if time.time()-self.heartbeat > 60 and time.time()-self.heartbeat_cooldown > 30:
            heartbeat_length = time.time()-self.heartbeat
            random_msg = "".join([chr(random.randint(64,125)) for _ in range(30)])
            while time.time()-self.command_delay < 0.5: time.sleep(0.7)
            self.chat(f"/msg {self.username} HeartBeat-KeepAlive {random_msg}",0.3) # sends a random message to the bot to make sure it's running / connected
            self.heartbeat_cooldown = time.time()
            self.chat("/whereami",0.2)

            self.quota = utils.load_obj("quota")
            utils.combine_dict(self.quota,self.quotaChange)
            utils.save_obj(self.quota,"quota")
            self.quotaChange = {}

            load = round((self.current_load/self.rate)*100)
            if self.current_load > self.rate:
                logging.info("Overloaded!")
            else:
                logging.info(f"Bot Load peaked at {load}%.")
            self.current_load = 0

            logging.info(f"Heartbeat ({int(heartbeat_length)}sec)")
            return
    
    def tick(self):
        self.heartbeat_tick()
        try:
            self.party_tick()
            self.msg_tick()
            self.command_tick()
            self.cooldown_tick()
        except Exception as error:
            logging.warning(error)

# contains the while loops that run the bot
class thread:
    def __init__(self,email,password,username):
    # define objects
        self.email = email
        self.password = password
        self.username = username

    def start(self):
        while True:
            try:
                # starts the bot and connects to the server *hence initialize*
                self.bot = bot(self.email,self.password,self.username)
                self.bot.initialize()
                while True:
                    try:
                        # ticks the bot continuously every 1/20th of a second
                        time.sleep(0.05)
                        self.bot.tick()
                    except Exception as error:
                        logging.warning("Unknown Error! " + str(error))
            except Exception as error:
                logging.warning("Unknown Error! " + str(error))

class thread:
    def __init__(self,email,password,username,rate):
        self.email = email
        self.password = password
        self.username = username
        self.rate = rate

        self.mutedelay = 0

    def start(self):
        while True:
            try:
                # starts the bot and connects to the server *hence initialize*
                self.bot = bot(self.email,self.password,self.username,self.rate)
                self.bot.initialize()
                while True:
                    try:
                        time.sleep(0.05)
                        self.bot.tick()
                        if self.bot.muted:
                            if int(self.bot.unmute_time-time.time()) > 0:
                                if time.time() - self.mutedelay >= 360:
                                    self.mutedelay = time.time()
                                    logging.critical("Muted: " + str(self.bot.mute_duration))
                            else:
                                self.muted = self.bot.muted = False
                    except Exception as error:
                        logging.warning(error)
                        self.bot.disconnect()
            except Exception as error:
                self.bot = None
                logging.warning(error)
                time.sleep(120)
