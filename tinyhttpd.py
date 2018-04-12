#coding : utf-8
"""
A simple httpserver just for fun.
What it does:
    1. Accept the request from browse.
    2. Get the request infomation(e.g request methond, request url ect).
    3. Call the right function to generate html file according to the url.
    4. Response. Send the html file to the request browse.
"""

import socket
import sys
import threading
from time import sleep

class SocketHandle(object):
    """
    This class is used to get socket send data.
    """

    def __init__(self, socket = None):
        if socket is None:
            self.socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM )
        else:
            self.socket = socket

    def recvMsg(self, msgLengths = None):
        chucks = []
        if msgLengths:
            bytesRecvd = 0
            while bytesRecvd < msgLengths:
                chuck = self.socket.recv(min(msgLengths - bytesRecvd, 2048))
                if chuck == b'':
                    raise RuntimeError("socket connection broken")
                chucks.append(chuck)
                bytesRecvd += len(chuck)
        else:
            chucks =  self.socket.recv(2048)     

        return b''.join(chucks)
        
    def sendMsg(self,msg):
        msgLengths = len(msg)
        totalsent = 0
        while totalsent < msgLengths:
            sent = self.socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent += sent

class httpRequestHandle(SocketHandle):

    def __init__(self, (socket, address)):
        if socket is None:
            raise RuntimeError("socket is None")
        super(httpRequestHandle,self).__init__(socket)
        self.address = address

    @classmethod
    def parseHttpRequest(cls,data):
        print(data) 

    def response(self):
        data = self.recvMsg()
        self.parseHttpRequest(data)
        htmlstr = """
                HTTP/1.1 200 OK
                Date: Sat, 31 Dec 2018 23:59:59 GMT
                Content-Type: text/html;charset=ISO-8859-1
                Content-Length: 122
                <html>
                <head>
                <title>Wrox Homepage</title>
                </head>
                <body>
                <h1> Hello World </h1> 
                </body>
                </html>
                """
        self.sendMsg(htmlstr)


MAX_CLIENT_CONNECTION = 10
config = ("localhost",8080)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(config)

print("Server listening...")
server.listen(MAX_CLIENT_CONNECTION)


while True:
    print("waitting for client...")
    handle = httpRequestHandle(server.accept())
    td = threading.Thread(target=handle.response)
    td.run()





