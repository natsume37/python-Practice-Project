# -*-coding:utf-8 -*-

"""
# File: 01-服务端.py
# Time: 2025/9/22 17:19
# Author:   Martin
# Description:  
"""
import socket

# 流式协议（TCP）
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定地址
sk.bind(('127.0.0.1', 8088))

sk.listen(5)
print("服务端开启成功")

conn,addr = sk.accept()
print("连接对象",conn)
print("连接地址",addr)
data = conn.recv(1024)
data = data.decode("utf-8")
print('客户端数据：',data)
conn.send(data.upper().encode('utf-8'))
conn.close()
sk.close() # 可选

