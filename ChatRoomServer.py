'''
server usage:
python server.py [ip address] [port]
'''

import socket
import time
import sys

UDP_IP= 'localhost'
UDP_PORT= 5432

#  create a datagram socket 
sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP

#  bind the socket to a port, to allow people to send info to it
sock.bind( (UDP_IP,UDP_PORT) )

#  keep a list of "connected" clients, even though we're not really
#  accepting connections per se. The purpose of this is to allow us
#  to replay chat messages to other people and
#  to see who's in the chatroom, etc
clients = []

#  this function sends a message to everyone who is "connected"
def broadcast(username,data):
  global clients
  for client in clients:
    if client[0] != username:
        sock.sendto(data, client[1])

#  main loop for the server
#  in this loop we try to receive data on the socket
#  and then we relay the message to other clients
while True:
    data = None
    message = None
    try:
        # try to get a message on the socket
        data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
        #  if there's a message, then parse it and add the client to the list
        #  if they're a new client
        
        message = data.decode()
        message_split = message.split(":")
        potential_client = (message_split[0], addr)
        username_taken = False
        returning_user = False
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
    #  if no message was available, just wait a while
    except socket.error:

      # wait a bit to keep from clobbering the CPU
      time.sleep(0.01)

    if data and (returning_user or not username_taken):
        message = data.decode()
        print(message)
        print(clients)
        message_split = message.split(":")
        #  the welcome message announces a new user to the clients
        if(message_split[1] == "@_@join"):
            welcome_message = message_split[0]+" has joined the chatroom" 
            broadcast( message_split[0], welcome_message.encode() )
        #  the /who message is only echoed back to the client who sent it
        #  The response is a list of other people in the chat room
        elif ( message_split[1] == "@_@leave" ):
            goodbye_message = message_split[0]+" has left the chatroom" 
            broadcast( message_split[0], goodbye_message.encode() )
            clients.remove(client)
        #  All other messages are simply re-broadcasted back to all clients
        else:
            broadcast(message_split[0], message.encode())