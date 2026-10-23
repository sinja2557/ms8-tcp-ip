import socket
import threading
import queue

SERVER_IP = "0.0.0.0" # All ip
SERVER_PORT = 50005

clients = []
q = queue.Queue()

def handle(conn, addr):
    print(addr, "입장 (현재", len(clients), "명)\n")
    
    while True:
        try:
            data = conn.recv(1024)

        except OSError:
            break

        if not data:
            break

        text = f"[{addr[0]}:{addr[1]}] {data.decode()}"
        q.put((conn, text))
        
    clients.remove(conn)
    conn.close()
    print(addr, "퇴장 (현재", len(clients), "명)\n")

def broadcast():
    while True:
        sender, text = q.get()
        print(text)

        for c in clients:
            if c != sender:
                try:
                    c.send(text.encode())

                except OSError:
                    pass

threading.Thread(target=broadcast, daemon=True).start()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()
print("Chat server started - wating connecting...\n")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle, args=(conn, addr), 
                     daemon=True).start()