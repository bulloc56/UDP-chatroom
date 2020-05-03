import socket
import os
import sys
import threading
import time

bad_username = False
Muted = False
blocklist = []
server_ip = 'localhost'
server_port = 5432
username = input('enter your username: ')
sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP

join_message = username+":@_@join"
sock.sendto( join_message.encode(), (server_ip, server_port) )

def get_messages():
  global sock, username, Muted, blocklist, bad_username
  while True:
    data = None
    try:
      data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
    except socket.error:
      # wait a bit
      time.sleep(0.01)
    if data and not Muted:
        #print data
        message = data.decode()
        split_message = message.split(":")
        if (message == "Username taken. Choose a different username."):
            bad_username = True
            print(message)
        elif (split_message[0] not in blocklist):
            print(message)

def get_input():
    global sock, username, Muted, blocklist, bad_username
    while True:
        user_input = input()
        if (bad_username):
            username = input("Enter a different username: ")
            join_message = username+":@_@join"
            sock.sendto( join_message.encode(), (server_ip, server_port) )
            bad_username = False
        else:
            if (user_input == "@_@leave"):
                message = username+":"+user_input
                sock.sendto( message.encode(), (server_ip, server_port) )
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

x = threading.Thread(target=get_input, args=())    
x.start()

y = threading.Thread(target=get_messages, args=())
y.start()
