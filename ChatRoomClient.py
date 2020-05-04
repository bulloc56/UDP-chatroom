import socket
import os
import sys
import threading
import time

# Some variables to help out keeping track of conditions
bad_username = False
Muted = False
blocklist = []
server_ip = 'localhost'
server_port = 5432
# on running the program, users will be asked to provide a username (which must be unique)
username = input('enter your username: ')
username = username.replace(":","")
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
# try to join the client list on the server
join_message = username+":@_@join"
sock.sendto( join_message.encode(), (server_ip, server_port) )
# function to run on one thread, gets messages and prints them if not muted
# and originating user is not on the blocklist
def get_messages():
  global sock, username, Muted, blocklist, bad_username
  while True:
    data = None
    try:
      data, addr = sock.recvfrom( 1024 ) 
    except socket.error:
      # error catching
      time.sleep(0.01)
    if data and not Muted:
        #print data
        message = data.decode()
        split_message = message.split(":")
        if (message == "Username taken. Choose a different username."):
            # set this variable so get_input knows it has to ask for a new username
            bad_username = True
            print(message)
        elif (split_message[0] not in blocklist):
            print(message)

def get_input():
    global sock, username, Muted, blocklist, bad_username
    while True:
        # gets the user input
        user_input = input()
        if (bad_username):
            # try joining client list again with a different username
            username = input("Enter a different username: ")
            username = username.replace(":","")
            join_message = username+":@_@join"
            sock.sendto( join_message.encode(), (server_ip, server_port) )
            bad_username = False
        else:
            # all options for a user
            if (user_input == "@_@leave"):
                message = username+":"+user_input
                sock.sendto( message.encode(), (server_ip, server_port) )
                # exits the program
                os._exit(1)
            elif (user_input == "@_@mute"):
                Muted = True
            elif (user_input == "@_@unmute"):
                Muted = False
            elif ("@_@block" in user_input):
                blocked_input = user_input.split(":")
                blocklist.append(blocked_input[1])
            elif ("@_@unblock" in user_input):
                blocked_input = user_input.split(":")
                if blocked_input[1] in blocklist:
                    blocklist.remove(blocked_input[1])
            else:
                message = username+":"+user_input
                sock.sendto( message.encode(), (server_ip, server_port) )
#start get_input thread
x = threading.Thread(target=get_input, args=())    
x.start()
#start the get_messages thread, both will terminate upon os._exit(1)
y = threading.Thread(target=get_messages, args=())
y.start()
