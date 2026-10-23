import socket
import threading
import queue

clients = []
q = queue.Queue()

def handle(conn, addr):
    print(addr, "입장 (현재", len(clients), "명")
    while True:
        try:
            data = conn.recv(1024)
        except OSError:
            pass