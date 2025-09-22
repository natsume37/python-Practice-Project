# -*-coding:utf-8 -*-

"""
# File: 01-客户端.py
# Time: 2025/9/22 20:37
# Author:   Martin
# Description:  
"""
import socket

# 流式协议（TCP）
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sk.connect(('127.0.0.1', 8088))

# 传输数据
sk.send('hello'.encode('utf-8'))
data = sk.recv(1024)
print(data.decode('utf-8'))

sk.close() # 必写