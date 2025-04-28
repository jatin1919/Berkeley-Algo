import socket
import time

class BerkeleyClient:
    def __init__(self, server_host='127.0.0.1', server_port=5000):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_host, server_port))
        print(f"Connected to server at {server_host}:{server_port}")

    def listen_for_commands(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message.startswith("GET_TIME"):
                    local_time = time.time()
                    self.client_socket.send(str(local_time).encode())
                elif message.startswith("ADJUST_TIME"):
                    _, adjustment = message.split('|')
                    adjustment = float(adjustment)
                    adjusted_time = time.time() + adjustment
                    print(f"Adjusted local time: {adjusted_time}")
            except Exception as e:
                print(f"Connection error: {e}")
                break

    def start(self):
        self.listen_for_commands()

if __name__ == "__main__":
    client = BerkeleyClient()
    client.start()
