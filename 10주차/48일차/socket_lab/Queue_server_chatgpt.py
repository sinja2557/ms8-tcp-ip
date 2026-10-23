
import socket
import threading
import queue

SERVER_IP = "0.0.0.0"
SERVER_PORT = 50005

clients = []
clients_lock = threading.Lock()
q = queue.Queue()
shutdown_event = threading.Event()
had_client = False


def handle(conn, addr):
    global had_client

    with clients_lock:
        had_client = True
        count = len(clients)

    print(f"{addr} 입장 (현재 {count}명)")

    try:
        while not shutdown_event.is_set():
            try:
                data = conn.recv(1024)
            except OSError:
                break

            if not data:
                break

            text = f"[{addr[0]}:{addr[1]}] {data.decode()}"
            q.put((conn, text))

    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
            count = len(clients)

        try:
            conn.close()
        except OSError:
            pass

        print(f"{addr} 퇴장 (현재 {count}명)")

        # 한 번이라도 접속한 클라이언트가 모두 퇴장하면 종료
        if had_client and count == 0:
            print("모든 클라이언트가 퇴장했습니다. 서버를 종료합니다.")
            shutdown_event.set()


def broadcast():
    while not shutdown_event.is_set():
        try:
            sender, text = q.get(timeout=0.5)
        except queue.Empty:
            continue

        print(text)

        # with clients_lock:
        #     targets = [c for c in clients if c != sender]

        # for c in targets:
        #     try:
        #         c.sendall(text.encode())
        #     except OSError:
        #         pass
        # 보낸 사람을 포함한 모든 클라이언트에게 전송
        with clients_lock:
            targets = list(clients)

        for c in targets:
            try:
                c.sendall(text.encode())
            except OSError:
                pass

        q.task_done()


threading.Thread(target=broadcast, daemon=True).start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()
server.settimeout(1.0)

print("Chat server started - waiting for connections...")

try:
    while not shutdown_event.is_set():
        try:
            conn, addr = server.accept()
        except socket.timeout:
            continue
        except OSError:
            break

        with clients_lock:
            if shutdown_event.is_set():
                conn.close()
                break
            clients.append(conn)

        threading.Thread(
            target=handle,
            args=(conn, addr),
            daemon=True
        ).start()

finally:
    shutdown_event.set()

    with clients_lock:
        remaining = list(clients)
        clients.clear()

    for c in remaining:
        try:
            c.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            c.close()
        except OSError:
            pass

    server.close()
    print("서버가 종료되었습니다.")
