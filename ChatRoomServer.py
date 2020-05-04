#Kevin Bullock ChatRoomServer.py

import socket
import time
import sys

UDP_IP= 'localhost'
UDP_PORT= 5432

#  socket setup
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) 
sock.bind( (UDP_IP,UDP_PORT) )

#  list of clients
clients = []

#  send data to all clients except the client with the username specified
def broadcast(username,data):
  global clients
  for client in clients:
    if client[0] != username:
        sock.sendto(data, client[1])

#  Loop forever, if data arrives process it
while True:
    data = None
    message = None
    try:
        # message
        data, addr = sock.recvfrom( 1024 ) 
        # decode the message and split it
        message = data.decode()
        message_split = message.split(":")
        # don't know if this is new or returning client
        potential_client = (message_split[0], addr)
        username_taken = False
        returning_user = False
        user_added = False
        # check if username is present, if it is, check if it is a returning user or a duplicate
        #if duplicate, client has to choose a differnet username 
        for client in clients:
            if client[0] == message_split[0]:
                username_taken = True
                if client == potential_client:
                    returning_user = True      
        if username_taken and not returning_user:
            message = "Username taken. Choose a different username."
            sock.sendto(message.encode(), addr)
            username_taken = False
        elif not username_taken and not returning_user:
            clients.append(potential_client)
            user_added = True
    #  if data is not in right format or some other error
    except socket.error:
      time.sleep(0.01)
    # only send messages if it comes from client in the list
    if data and (returning_user or user_added):
        message = data.decode()
        print(message)
        print(clients)
        message_split = message.split(":")
        #  the welcome message announces a new user to the clients
        if(message_split[1] == "@_@join"):
            welcome_message = message_split[0]+" has joined the chatroom" 
            broadcast( message_split[0], welcome_message.encode() )
        #the goodbye_message announces a returning user has left the chatroom
        elif ( message_split[1] == "@_@leave" ):
            goodbye_message = message_split[0]+" has left the chatroom" 
            broadcast( message_split[0], goodbye_message.encode() )
            clients.remove(potential_client)
        #  any other messages are sent to all broadcast to the intended clients
        else:
            broadcast(message_split[0], message.encode())