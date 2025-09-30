# -*- coding: utf-8 -*-
"""
@File    : 11-tcp客户端.py
@Author  : Martin
@Time    : 2025/9/30 22:42
@Desc    : 
"""
import socket
import time

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(("127.0.0.1", 8081))

while True:
    c.send(b"hello")
    data = c.recv(1024)
    print(data.decode("utf-8"))
    time.sleep(2)
