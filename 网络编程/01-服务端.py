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
print("TCP服务器已开启.....")
sk.listen(5)

# 持续提供服务
while True:
    conn,addr = sk.accept()
    print("连接对象:",conn)
    print("客户端ip+port",addr)
    while True:
        try: # 异常断开、windows直接报错问题
            data = conn.recv(1024)
        except socket.error:
            break
        if not data: # mac/linux解决异常断开收空问题
            break
        data = data.decode("utf-8")
        print('客户端数据：',data)
        conn.send(data.upper().encode('utf-8'))
    conn.close()
sk.close() # 可选

