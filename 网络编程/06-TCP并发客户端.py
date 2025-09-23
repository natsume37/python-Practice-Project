# -*-coding:utf-8 -*-

"""
# File: 01-客户端.py
# Time: 2025/9/22 20:37
# Author:   Martin
# Description:  客户端不需要改变
"""
import socket

# 流式协议（TCP）
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sk.connect(('127.0.0.1', 8088))
while True:
    msg = input("请输入数据>>> ").strip()
    if not msg:
        continue
    # 传输数据
    sk.send(msg.encode('utf-8'))
    if msg.lower() == 'q':
        break
    data = sk.recv(1024)
    print(data.decode('utf-8'))

sk.close()  # 必写
