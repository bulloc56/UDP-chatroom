import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Server:Socket Created')

host = 'localhost'
port = 5433

message = 'hello'

try:
    print('Client'+message)
    client_socket.sendto(message.encode(), (host,5432))

    data, server = client_socket.recvfrom(4096)
    data = data.decode()
    print('Client' + data)
finally:
    print('Client closing socket')
    client_socket.close()