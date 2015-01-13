#!/usr/bin/python3

import ts3
import webbrowser
import psutil

# Data
USER = "REPLACE_ME"
PASS = "REPLACE_ME"
HOST = "0.0.0.0"
PORT = 10011
# Bot config
CHANNEL = "Sala Sagres"
SEQ = "ze:https://www.youtube.com/"
SEQ_SIZE = 27

# Browser config
BROWSER_PROC_NAME = "chrome"


def youtube_opener(sender, event):
    try:
        # get the msg attr
        msg = event.parsed[0]['msg']
        channel_id = ts3conn.channelfind(pattern=CHANNEL)[0]['cid']

        # if the initial part matches the sequence
        if(msg[0:SEQ_SIZE] == SEQ):
            ts3conn.sendtextmessage(
                targetmode=2,
                target=channel_id,
                #msg="No, Siñor Peter no esta!")
                msg="♬ ♭ ♮ ♩ ♪ ♫  ♯")
            return
            # kill the browser
            for proc in psutil.process_iter():
                if proc.name() == BROWSER_PROC_NAME:
                    proc.kill()

            # reopen browser with link
            webbrowser.open(msg[4:], new=0, autoraise=True)
        elif(msg[0:3] == "ze:"):
            ts3conn.sendtextmessage(
                targetmode=2,
                target=channel_id,
                #msg="No, Siñor Peter no esta!")
                msg="Usage: ze:https://www.youtube.com/<some_video>")
        else:
            print(msg[0:7])
    except:
        print("Some strange message was received.")

with ts3.query.TS3Connection(HOST) as ts3conn:
    ts3conn.login(client_login_name=USER,
                  client_login_password=PASS)
    # Set use mode of connection
    ts3conn.use(sid=1)
    # Get own ID and channel ID
    me = ts3conn.whoami()[0]['client_id']
    ts3conn.clientupdate(clid=me, CLIENT_NICKNAME="Zé Bot")
    channel_id = ts3conn.channelfind(pattern=CHANNEL)[0]['cid']
    # Move the bot to the channel
    ts3conn.clientmove(cid=channel_id, clid=me)

    # Register notifs and handle in new thread
    ts3conn.servernotifyregister(event="textchannel", id_=channel_id)
    ts3conn.on_event.connect(youtube_opener)
    ts3conn.recv_in_thread()

    # To finish the bot press Enter
    input("> Hit enter to finish.\n")
