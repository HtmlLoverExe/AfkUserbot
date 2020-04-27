"""
Edit This
"""
apiId = 1303237
apiHash = "1c971e44ddd29077abf386b0c47c5a03"

"""
Afk message. {original_msg} is the text
of message sent by the user
"""
afkMessage = "Scusa al momento non sono disponibile.\n" \
             "Your message got saved here:\n" \
             "\n" \
             "{original_msg}\n" \
             "\n" \
             "Only one message in every 30 seconds will be saved.\n" \
             "<a href=\"https://github.com/GodSaveTheDoge/AfkUserbot\">Create your own</a>"

"""
Boring stuff
"""

import os
import time
from datetime import datetime
from pathlib import Path
import requests
from pyrogram import Client, Filters, Emoji
from pyrogram.errors import *


users = {}
afk = False
accepted_users = []
banned_users = []
bot = Client(
    "UserbotAfk",
    api_id=apiId,
    api_hash=apiHash)


@bot.on_message(Filters.private)
def check_saved(Client, msg):
    global users
    if not msg.from_user.id in users:
        users[msg.from_user.id] = 0
    msg.continue_propagation()


@bot.on_message(Filters.private & ~Filters.user("self"))
def logger(Client, msg):
    print("[PM] Got a new message from: {}. Text: {}".format(
        "@" + msg.from_user.username if msg.from_user.username else msg.from_user.first_name,
        str(msg.text)[0:20]))
    msg.continue_propagation()


@bot.on_message(Filters.user("self") & Filters.command("afk", prefixes=[".", "/", "!", "#"]))
def afk_command(Client, msg):
    global afk
    if len(msg.command) == 1:
        msg.edit_text("You are afk" if afk else "You are not afk")
    else:
        if msg.command[1] == "on":
            afk = True
            msg.edit_text("Afk enabled.")
        elif msg.command[1] == "off":
            afk = False
            msg.edit_text("Afk disabled.")
        else:
            msg.edit_text("You are afk" if afk else "You are not afk")


@bot.on_message(Filters.user("self") & Filters.command("accept", prefixes=[".", "/", "!", "#"]))
def accept_command(Client, msg):
    global accepted_users
    accepted_users.append(msg.chat.id)
    msg.edit_text("Accepted {}.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & Filters.command("ban", prefixes=[".", "/", "!", "#"]))
def accept_command(Client, msg):
    global banned_users
    banned_users.append(msg.chat.id)
    if msg.chat.id in accepted_users: accepted_users.remove(accepted_users)
    msg.edit_text("Ehy testa di cazzo, sei stato bannato {}.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & Filters.command("unaccept", prefixes=[".", "/", "!", "#"]))
def accept_command(Client, msg):
    global accepted_users
    accepted_users.remove(msg.chat.id)
    msg.edit_text("Removed {} from accepted list.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & Filters.command("unban", prefixes=[".", "/", "!", "#"]))
def accept_command(Client, msg):
    global banned_users
    banned_users.remove(msg.chat.id)
    if msg.chat.id in accepted_users: accepted_users.remove(accepted_users)
    msg.edit_text("Unbanned {}.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & Filters.command("commands", prefixes=[".", "/", "!", "#"]))
def commands_command(Client, msg):
    msg.edit_text("Avaiable Commands:\n"
                  "/afk - see if you are afk\n"
                  "/afk on - turn on afk\n"
                  "/afk off - turn off afk\n"
                  "/accept - in private, this person can now talk as much as he wants\n"
                  "/ban - in private, every message will be deleted and he'll not get any answer\n"
                  "\n"
                  "Prefixes: . / ! #")


@bot.on_message(Filters.private & ~Filters.user("self"))
def on_private_afk_message(Client, msg):
    if not msg.from_user.id in accepted_users:
        if afk:
            msg.delete()
            if users[msg.from_user.id] + 30 < int(time.time()) and not msg.from_user.id in banned_users:
                bot.send_message(msg.chat.id,
                                 afkMessage.replace("{original_msg}", str(msg.text)),
                                 disable_web_page_preview=True)
                users[msg.from_user.id] = int(time.time())
                
                
@bot.on_message(Filters.user("self") & Filters.command("show", prefixes=["!", "/", ".", "#"]))
def show_command(c, msg):
    if len(msg.command) < 2:
        msg.edit_text("What should I send?\n<code>/show my text</code>")
    tosend = " ".join(msg.command[1:])
    for i in range(len(tosend)):
        if tosend[i] == " ":
            time.sleep(0.5)
            continue
        msg.edit_text(tosend[:i+1])
        time.sleep(0.3)

     
    flood_timeout = 1


@bot.on_message(Filters.user("self") & Filters.command("flood", prefixes=[".", "/", "!", "#"]))
def flood_command(c, msg):
    if len(msg.command) < 3:
        msg.edit_text(f"{Emoji.CROSS_MARK} Please use: \n<code>/flood amount text</code>")
        return 1
    amount = msg.command[1]
    text = " ".join(msg.command[2:])
    try:
        amount = int(amount)
    except ValueError:
        msg.edit_text(f"{Emoji.CROSS_MARK} Value Error: {amount} is not a valid number.")
        return
    msg.edit_text(f"{Emoji.HEAVY_MINUS_SIGN} Started...")
    c = 0
    for i in range(amount):
        try:
            bot.send_message(msg.chat.id, text)
        except FloodWait as e:
            print(f"Sleeping {e.x} seconds.")
            time.sleep(e.x)
        c += 1
        time.sleep(0.1)
        msg.edit_text(
            f"{Emoji.HEAVY_MINUS_SIGN} Started...\n{Emoji.HOURGLASS_NOT_DONE} Timeout: {flood_timeout} \n{Emoji.MOBILE_PHONE_WITH_ARROW} Messages Sent: {c}")
        time.sleep(flood_timeout)
    msg.edit_text(
        f"{Emoji.HEAVY_CHECK_MARK} Done!\n{Emoji.HOURGLASS_DONE} Timeout: {flood_timeout} \n{Emoji.MOBILE_PHONE_WITH_ARROW} Messages Sent: {c}")


@bot.on_message(Filters.user("self") & Filters.command("setfloodtimeout", prefixes=[".", "/", "!", "#"]))
def setfloodtimeout_command(c, msg):
    global flood_timeout
    if len(msg.command) < 2:
        msg.edit_text(
            f"{Emoji.CROSS_MARK} Please Use:\n<code>/setfloodtimeout timeout</code>\nNote: timout needs to be in seconds.")
        return 1
    timeout = msg.command[1]
    try:
        flood_timeout = float(timeout)
    except ValueError:
        msg.edit_text(f"{Emoji.CROSS_MARK} Value Error: {timeout} is not a valid number.")
    else:
        msg.edit_text(f"{Emoji.HEAVY_CHECK_MARK} Timeout set to: {timeout} seconds.")
      
bot.run()
