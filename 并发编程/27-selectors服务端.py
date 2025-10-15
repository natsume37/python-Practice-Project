# -*- coding: utf-8 -*-
"""
@File    : 27-selectors服务端.py
@Author  : Martin
@Time    : 2025/10/13 17:39
@Desc    : selectors库
根据操作系统自动匹配合适的代码方案
"""
import socket
import selectors


def accept(server):
    conn, addr = server.accept()
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn):
    try:
        data = conn.recv(1024)
        if not data:
            conn.close()
            sel.unregister(conn)
            return
        conn.send(data.upper())
    except ConnectionResetError:
        conn.close()
        sel.unregister(conn)
        return


server = socket.socket()
server.bind(("127.0.0.1", 8081))
server.listen(5)
server.setblocking(False)  # 设置非阻塞

sel = selectors.DefaultSelector()
sel.register(server, selectors.EVENT_READ, accept)

while True:
    # 循环接受可处理的任务
    events = sel.select()
    for key, mask, in events:
        callback = key.data
        callback(key.fileobj)
