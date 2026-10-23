import socket
import threading

SERVER_IP = "0.0.0.0" # All ip
SERVER_PORT = 50005

clients = []

def handle(conn, addr):
    print(addr, "입장 (현재", len(clients), "명")
    
    while True:
        try:
            data = conn.recv(1024)
        
        except OSError:
            break

        if not data:
            break

        text = f"[{addr[[0]]}:{addr[1]}] {data.decode()}"
        print(text)
        for c in clients:
            if c != conn:
                try:
                    c.send(text.encode())
                except OSError:
                    pass

    clients.remove(conn)
    conn.close()
    print(addr, "퇴장 (현재", len(clients), "명")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()
print("Chat server started - wating connecting...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle, args=(conn, addr), 
                     daemon=True).start()
