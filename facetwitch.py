import socket
import sys
import time
import threading
from fbchat import Client
from fbchat.models import *

# Dina cookies
cookies = {
    "c_user": "<fb bot c_user number>",
    "xs": "<xs string>"
}

# Användarens ID att skicka meddelanden till
user_id = "<your own fb c_user number>"

server = "irc.chat.twitch.tv"
channel = "<channel>" # exempel #synt_haren
botnick = "<twitch user name>"
password = "oauth:<oauth>"

while True:
    try:
        # Skapa en ny klient och logga in med cookies
        print("Logging in to Facebook...")
        client = Client("", "", session_cookies=cookies)
        break  # If login is successful, break the loop
    except Exception as e:
        print("Login failed, retrying in 5 seconds...")
        time.sleep(5)  # Wait for 5 seconds before retrying

while True:
    try:
        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("connecting to:" + server)
        irc.connect((server, 6667))

        irc.send(bytes("PASS " + password + "\n", "UTF-8"))
        irc.send(bytes("NICK " + botnick + "\n", "UTF-8"))

        time.sleep(5)  # Wait for 5 seconds

        irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))
        break  # If connection is successful, break the loop
    except (ConnectionResetError, OSError) as e:
        print("Connection failed, retrying in 5 seconds...")
        time.sleep(5)  # Wait for 5 seconds before retrying

def quit():
    print("Quitting...")
    irc.send(bytes("QUIT \n", "UTF-8"))
    client.logout()  # Log out from fbchat
    sys.exit()

# Function to check for new messages from the Facebook user
def check_fb_messages():
    last_message_id = None

    while True:
        # Fetch the latest message from the Facebook user
        messages = client.fetchThreadMessages(thread_id=user_id, limit=1)
        latest_message = messages[0]

        # If this is a new message and it has text, send it to the IRC channel
        if latest_message.uid != last_message_id and latest_message.text is not None:
            # Check if the message was sent by the Facebook user
            if latest_message.author == user_id:
                irc.send(bytes("PRIVMSG " + channel + " :" + latest_message.text + "\n", "UTF-8"))
                last_message_id = latest_message.uid

        time.sleep(1)  # Wait for 1 second

# Start the background thread
threading.Thread(target=check_fb_messages).start()

try:
    while True:
        text = irc.recv(2040).decode("UTF-8")
        print(text)

        if "PING" in text:
            irc.send(bytes("PONG :tmi.twitch.tv\r\n", "UTF-8"))
        elif "PRIVMSG" in text:
            # Extract the username and message
            username = text.split('!', 1)[0][1:]
            message = text.split('PRIVMSG', 1)[1].split(':', 1)[1]

            # Format the message
            formatted_message = f"{username}: {message}"

            # Send the message to the Facebook user
            client.send(Message(text=formatted_message), thread_id=user_id, thread_type=ThreadType.USER)

except KeyboardInterrupt:
    quit()
