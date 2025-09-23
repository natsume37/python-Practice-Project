# -*- coding: utf-8 -*-
"""
@File    : 03-CMD客户端.py.py
@Author  : Martin
@Time    : 2025/9/23 12:08
@Desc    : 
"""
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8081))
while True:
    cmd = input("请输入终端命令>>> ").strip()
    if not cmd:
        continue
    client.send(cmd.encode('utf-8'))
    # 收取header（长度8字节）
    data_size = int(client.recv(1024).decode('utf-8'))
    recv_size = 0
    # 小数据定义变量、大数据的话要用文件！
    data = b''
    while recv_size<data_size:
        res = client.recv(1024)
        recv_size += len(res)
        data += res

    print(data.decode('utf-8'))
    print(data_size)
