# -*- coding: utf-8 -*-
"""
@File    : 22-tcp服务端.py
@Author  : Martin
@Time    : 2025/10/4 13:30
@Desc    : 
"""
import socket
from threading import Thread



def comm(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(data.upper())
        except:
            break
    conn.close()

def run(ip, port):
    sk = socket.socket()
    sk.bind((ip, port))
    sk.listen(5)
    while True:
        conn, addr = sk.accept()
        Thread(target=comm, args=(conn,)).start()

if __name__ == '__main__':
    run("127.0.0.1", 8081)