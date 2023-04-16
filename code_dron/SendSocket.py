# This Python file uses the following encoding: utf-8
import socket
import sys
import json


class SendSocket:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            # Connect to server and send data
            self.sock.connect((HOST, PORT))
        self.sock.settimeout(2)

    def send_data(self, array):
        data = json.dumps(array)
        self.sock.sendall(bytes(data + "\n", "utf-8"))
