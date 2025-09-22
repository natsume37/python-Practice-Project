# -*- coding: utf-8 -*-
"""
@File    : 02-udp服务端.py
@Author  : Martin
@Time    : 2025/9/22 22:51
@Desc    : 
"""
import socket

# 流式协议（udp）
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定地址
sk.bind(('127.0.0.1', 8088))
print("UDP服务器已开启.....")

# 持续提供服务

while True:

    data,addr = sk.recvfrom(1024)
    print('客户端数据：',data)
    sk.sendto(data.upper(), addr)

sk.close() # 可选