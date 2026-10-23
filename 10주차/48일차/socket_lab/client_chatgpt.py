
import socket
import threading
import msvcrt
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 50005

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

print("접속 완료. 접속 해제 입력: q")

screen_lock = threading.Lock()
input_buffer = ""
prompt = "Send to msg: "
running = threading.Event()
running.set()


def redraw():
    # 현재 입력 줄을 지우고 입력 내용을 다시 표시
    sys.stdout.write("\r\x1b[2K")
    sys.stdout.write(prompt + input_buffer)
    sys.stdout.flush()


def receive():
    global input_buffer

    while running.is_set():
        try:
            data = client.recv(1024)
        except OSError:
            break

        if not data:
            with screen_lock:
                print("\r\x1b[2KDisconnected from server...")
            break

        message = data.decode()

        with screen_lock:
            # 메시지를 현재 입력 줄 위에 표시
            sys.stdout.write("\r\x1b[2K")
            sys.stdout.write(message + "\n")
            redraw()

    running.clear()


threading.Thread(target=receive, daemon=True).start()

try:
    with screen_lock:
        redraw()

    while running.is_set():
        ch = msvcrt.getwch()

        with screen_lock:
            if ch in ("\r", "\n"):
                msg = input_buffer
                input_buffer = ""

                sys.stdout.write("\r\x1b[2K")
                sys.stdout.flush()

                if msg == "q":
                    running.clear()
                    break

                if msg:
                    try:
                        client.sendall(msg.encode())
                    except OSError:
                        running.clear()
                        break

                redraw()

            elif ch == "\x03":
                running.clear()
                break

            elif ch == "\b":
                input_buffer = input_buffer[:-1]
                redraw()

            elif ch in ("\x00", "\xe0"):
                # 방향키 등 확장 키는 무시
                msvcrt.getwch()

            elif ch.isprintable():
                input_buffer += ch
                redraw()

except (KeyboardInterrupt, OSError):
    pass

finally:
    running.clear()

    try:
        client.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass

    client.close()

    with screen_lock:
        print("\n연결을 종료했습니다.")
