# -*- coding: utf-8 -*-
"""
@File    : 26-selectors客户端.py
@Author  : Martin
@Time    : 2025/10/13 17:38
@Desc    : 
"""
import socket
import time

client = socket.socket()
client.connect(("127.0.0.1", 8081))

while True:
    time.sleep(1)
    client.send(b"hello")
    data = client.recv(1024)
    print(data)