# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 04:54:27 2023

@author: 2233a
"""
import socketserver
import json

class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data_recieved = self.rfile.readline().strip()
        self.data_recieved = json.loads(self.data_recieved.decode())
        
    def handle_timeout(self):
        print("tiempo de espera para recivir datos agotado")

if __name__ == "__main__":
    HOST, PORT = "localhost", 1046

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    