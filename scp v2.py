#import xsh.Session
#import xsh.Screen
#import xsh.Dialog

import sys
import os
import time
import logging
from datetime import datetime, date, timedelta
import re


# get_time = time.localtime()
# time_string = time.strftime("%m-%d-%Y", get_time)
time_string = time.strftime("%m-%d-%Y", time.localtime())
log_time = time.strftime("%m-%d-%Y_%H:%M:%S", time.localtime())

# loc = "C:\\Users\\ERASMDH\\Google Drive\\python\\xshell\\"
loc = os.getcwd() 
details_log = os.getcwd() + "\details_log_" + log_time + ".log"
command_log = ""
password = "Bangladesh_adm@43#21"
terminate = "\003"
command_count = 0


def log(level, msg, tofile=True):
    #print(msg)
    if tofile is True:
        if level == 0:
            logger.info(msg)
        else:
            logger.error(msg)


logger = logging.getLogger("cuarch")
hdlr = logging.FileHandler(details_log)
hdlr.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s"))
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

log(0, "Initialising...")

def get_choice():
    global commandfile
    global choice
    count = 0 

    choice = xsh.Dialog.Prompt("Insert Script No. I.e. 1 or 2 or 3 up to 9", "Input script", "", 0)
    try:
        choice = int(choice)
        commandfile = loc + "\scrip" + str(choice) + ".txt"

    except Exception as e:
        log(0, e)


def get_commands():
    with open(commandfile) as cf:
        return cf.readlines()


def get_current_row_info(num: int):
    screenRow = xsh.Screen.CurrentRow
    line = xsh.Screen.Get(screenRow, 1, screenRow, num)
    return line

def paste_command(command):
    line = get_current_row_info(100)
    log(0, line)
    if "$" in line:
        xsh.Screen.Send(command+"\r")
        log(0, command)
    else:
        xsh.Session.Sleep(5000)
        log(0, "Try again to paste command.")
        if xsh.Session.Connected:
            paste_command(command)
        else:
            log(1, "Session disconnected.")
            # xsh.Screen.Send(terminate)
            raise SystemExit

def paste_pass():
    line = get_current_row_info(100)
    log(0, line)
    if "password" in line:
        xsh.Screen.Send(password+"\r")

    else:
        xsh.Session.Sleep(2000)
        log(0, "Try again to paste password.")
        if xsh.Session.Connected:
            paste_pass()
        else:
            log(1, "Session disconnected.")
            # xsh.Screen.Send(terminate)
            raise SystemExit


def Main():
    global command_count
    global choice

    get_choice()
    while(xsh.Session.Connected):
        if isinstance(choice, int) and choice >= 1 and choice <= 9:
            xsh.Screen.Synchronous = True
            xsh.Session.Sleep(1000)

            commands = get_commands()

            for command in commands:
                paste_command(command)
                xsh.Session.Sleep(1000)
                paste_pass()
                #log(0, "Break")
                command_count = command_count + 1
                #break
        else:
            log(1, "Session disconnected.")
            
        log(0, "Total command pasted: " +str(command_count))
        log(0, "End.")
        log(0, "-------------------------")
        xsh.Screen.Send(terminate)

    else:
        xsh.Dialog.MessageBox("Invalid choice, Please choose 1 or 2 or 3 up to 9.", "MessageBox", 0)
        log(0, "Invalid choice.")
        log(0, "End.")
        log(0, "-------------------------")
