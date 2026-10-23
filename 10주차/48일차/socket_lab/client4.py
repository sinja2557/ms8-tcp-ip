import socket
import threading

SERVER_IP = "127.0.0.1" # localhost
SERVER_PORT = 50005

def receive():
    while True:
        try:
            data = client.recv(1024)

        except OSError:
            break

        if not data:
            print("Disconnected to server...")
            break
        print(data.decode())


                              # Ipv6 AF_INET6  | Unix AF_UNIX
                              # UDP SOCK_DGRAM | SOCK_RAW IP Layer Protocol
                              # Ipv4 , TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT)) # IP, Port
print("접속 완료. \n접속 해제 : q")

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input("Client: ")
    if msg == "q":
        break

    client.send(msg.encode()) # Client send to Server

client.close() # client socket close 