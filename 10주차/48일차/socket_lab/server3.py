import socket

SERVER_IP = "0.0.0.0" # All ip
SERVER_PORT = 50005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()
print("접속을 기다립니다...")

while True:
    conn, addr = server.accept()
    print(addr, "에서 접속했습니다.")

    while True:
        data = conn.recv(1024)

        if not data:
            print(addr, "의 연결이 끊겼습니다.")
            break

        print("Receviced Msg:", data.decode())
        reply = input("Server: ")
        conn.send(reply.encode())

    conn.close()    # conn socket close 
server.close()  # server socket close 