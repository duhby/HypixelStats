# Run this file to start the program
import main     # main project file
import getpass  # allows password to be hidden during input

email = input('email: ')
password = getpass.getpass('password: ')
username = input('bot ign: ')
rate = input('rate (msgs per minute): ')

bot = main.thread(email,password,username,rate)
bot.start()
