import socket

SERVER_IP = "127.0.0.1" # localhost

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, 50005))

client.send("안녕하세요".encode())

data = client.recv()
print("서버 답장:", data.decode())

client.close()