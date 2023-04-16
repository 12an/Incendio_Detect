# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:42:45 2023

@author: 2233a
"""

import socketserver
import json
import socket

class CameraTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    imagen = list()
    temperatura = list()
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data_recieved = self.rfile.readline().strip()
        self.data_recieved = json.loads(self.data_recieved.decode())
        CameraTCPHandler.imagen = self.data_recieved.get("imagen")
        CameraTCPHandler.temperatura = self.data_recieved.get("temperatura")

    def handle_timeout(self):
        print("tiempo de espera para recivir datos agotado")


class InfoTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    porcentage_bateria = 0
    coordenadas = dict()
    altura = 0
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data_recieved = self.rfile.readline().strip()
        self.data_recieved = json.loads(self.data_recieved.decode())
        InfoTCPHandler.porcentage_bateria = self.data_recieved.get("porcentage_bateria")
        InfoTCPHandler.coordenadas = self.data_recieved.get("coordenadas")
        InfoTCPHandler.altura = self.data_recieved.get("altura")

    def handle_timeout(self):
        print("tiempo de espera para recivir datos agotado")


class SendComandSocket:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            # Connect to server and send data
            self.sock.connect((HOST, PORT))
        self.sock.settimeout(2)

    def send_data(self, comandos_dict):
        data = json.dumps(comandos_dict)
        self.sock.sendall(bytes(data + "\n", "utf-8"))
