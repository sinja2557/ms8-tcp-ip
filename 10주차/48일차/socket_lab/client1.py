import socket

SERVER_IP = "127.0.0.1" # localhost
SERVER_PORT = 50005

                              # Ipv6 AF_INET6  | Unix AF_UNIX
                              # UDP SOCK_DGRAM | SOCK_RAW IP Layer Protocol
                              # Ipv4 , TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT)) # IP, Port

client.send("안녕하세요 server".encode()) # Client send to Server

data = client.recv(1024) # server receive
print("Server:", data.decode())

client.close() # client close socket