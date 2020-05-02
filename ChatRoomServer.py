import socket;

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Server:Socket Created')

host = 'localhost'
port = 5432

server_socket.bind((host,port))
print('Server: Socket connected to' + host)

message = 'This is a message'

while True:
    data, addr = server_socket.recvfrom(4096)

    if data:
        print('Server: sending')
        server_socket.sendto(data + (message.encode()), addr)