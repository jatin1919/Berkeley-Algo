import socket
import threading
import time

class BerkeleyServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

    def accept_connections(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            print("Client connected.")
            self.clients.append(client_socket)

    def synchronize_clocks(self):
        total_time = 0
        active_clients = []
        server_time = time.time()  # Capture once!

        for client_socket in self.clients:
            try:
                client_socket.send(b"GET_TIME")
                client_time = float(client_socket.recv(1024).decode())
                total_time += client_time
                active_clients.append(client_socket)
                print(f"Received client time: {client_time}")
            except Exception as e:
                print(f"Error with client: {e}")
                client_socket.close()

        total_time += server_time
        average_time = total_time / (len(active_clients) + 1)
        adjustment = average_time - server_time
        print(f"Average time: {average_time}, Adjustment: {adjustment}")

        for client_socket in active_clients:
            try:
                # Send combined command + adjustment
                client_socket.send(f"ADJUST_TIME|{adjustment}".encode())
            except Exception as e:
                print(f"Error sending adjustment: {e}")
                client_socket.close()

    def start(self):
        threading.Thread(target=self.accept_connections, daemon=True).start()
        while True:
            command = input("Enter 'sync' to synchronize clocks or 'exit' to quit: ")
            if command == 'sync':
                self.synchronize_clocks()
            elif command == 'exit':
                break

if __name__ == "__main__":
    server = BerkeleyServer()
    server.start()
