# Run this file to start the program
import main     # main project file
import getpass  # allows password to be hidden during input

email = "email"
password = "password"
username = "ign"
rate = "25"

bot = main.thread(email,password,username,rate)
bot.start()
