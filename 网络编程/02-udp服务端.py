# -*- coding: utf-8 -*-
"""
@File    : 02-udp服务端.py
@Author  : Martin
@Time    : 2025/9/22 22:51
you@Desc    :
UDP 不会出现粘包问题
一个send对应一个recv
收不干净直接丢弃（mac\inux)
报错（Windows）

UDP最大传输 1472byte(稳定：512字节）
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