# -*- coding: utf-8 -*-
"""
@File    : 11-tcp服务端.py
@Author  : Martin
@Time    : 2025/9/30 22:34
@Desc    : 
"""
import socket
from multiprocessing import Process
from threading import Thread


def task(conn):
    while True:
        try:
            data = conn.recv(1024)
        except:
            break
        if not data:
            break
        print(data.decode("utf-8"))
        conn.send(data.upper())
    conn.close()


if __name__ == '__main__':
    # 默认tcp协议
    sk = socket.socket()
    sk.bind(("127.0.0.1", 8081))
    sk.listen(5)

    while True:
        print("服务器开启.....")
        conn, addr = sk.accept()
        p = Process(target=task, args=(conn,))
        p.start()