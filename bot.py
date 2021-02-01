# dubs#9025
# Hypixel Stats
# 2/1/21

##TODO: add logging
#import logging
import minecraft

class bot:
    def __init__(self,email,password,rate,admins):
        self.email = email
        self.password = password
        self.rate = rate
        self.admins = admins
    
    def login(self):
        ##
    
    def tick(self):
        ##


class thread:
    def __init__(self,email,password,rate,admins):
        self.email = email
        self.password = password
        self.rate = rate
        self.admins = admins

    def start():
        botInst = bot(self.email,self.password,self.rate,self.admins)
        botInst.login()
        while True:
            try: botInst.tick()
            except Exception as error: print(error)
            time.sleep(0.05)
