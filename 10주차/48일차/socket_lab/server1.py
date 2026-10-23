import socket

SERVER_IP = "0.0.0.0" # All ip
SERVER_PORT = 50005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()
print("접속을 기다립니다...")

conn, addr = server.accept()
print(addr, "에서 접속했습니다.")

data = conn.recv(1024)
print("받은 메세지:", data.decode())

conn.send("안녕하세요 client".encode())

conn.close()
server.close()