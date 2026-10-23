import socket

SERVER_IP = "10.10.34.4" # localhost
SERVER_PORT = 50005

                              # Ipv6 AF_INET6  | Unix AF_UNIX
                              # UDP SOCK_DGRAM | SOCK_RAW IP Layer Protocol
                              # Ipv4 , TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT)) # IP, Port
print("접속 완료. \n접속 해제 : q")

while True:
    msg = input("Client: ")
    if msg == "q":
        break

    client.send(msg.encode()) # Client send to Server

    data = client.recv(1024) # server receive
    if not data:
        print("Server closed.")
        break

    print("Receviced Msg:", data.decode())

client.close() # client socket close 