# -*- coding: utf-8 -*-
"""
@File    : 02-udp客户端.py
@Author  : Martin
@Time    : 2025/9/22 22:51
@Desc    : 
"""
import socket

# 流式协议（TCP）
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 可发空（桶装水、可发空桶）
while True:
    msg = input("请输入数据>>> ").strip()
    if msg.lower() == 'q':
        break
    sk.sendto(msg.encode('utf-8'),('127.0.0.1', 8088))
    # 传输数据
    data,addr = sk.recvfrom(1024)
    print(data)
sk.close()  # 必写