# This file is run to start the program
import main    # main project file
import getpass # allows password to be hidden during input

email = input('email: ')
password = getpass.getpass('password: ')
username = input('bot ign: ')

bot = start.thread(email,password,username)
bot.start()
