# -*- coding: utf-8 -*-
"""
@File    : 22-tcp客户端.py
@Author  : Martin
@Time    : 2025/10/4 13:36
@Desc    : 
"""
import socket
client = socket.socket()
client.connect(("127.0.0.1", 8081))

while True:
    client.send(b"hello")
    data = client.recv(1024)
    print(data)