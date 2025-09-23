# -*- coding: utf-8 -*-
"""
@File    : 03-CMD服务端.py
@Author  : Martin
@Time    : 2025/9/23 12:07
@Desc    : TCP（可靠一点）

TCP 有粘包问题需要解决
"""
import socket
import subprocess

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8081))

server.listen(5)
print("服务器开启....")
while True:
    conn, addr = server.accept()
    while True:
        try:
            cmd = conn.recv(1024)
        except socket.error as e:
            continue
        if not cmd:
            break
        # 处理CMD命令
        obj = subprocess.Popen(cmd.decode('utf-8'),
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE
                         )
        out_res = obj.stdout.read()
        err_res = obj.stderr.read()
        # 定义数据长度
        data_size = len(out_res) + len(err_res)
        # 定义协议（数据头）8个字节长度的数据头
        header = bytes(str(data_size), 'utf-8').zfill(8)
        # 发送数据头
        conn.send(header)
        print(header)
        conn.send(out_res)
        conn.send(err_res)

    conn.close()

"""
粘包问题
客户端收的太快、TCP底层的优化算法、将多个间隔小的数据一起发送
（方案一、发送和收取的数据量加大）
1. 收的太快（服务端的数据还未完全流入客户端）
2. 缓存太小（服务端数据还没传完、客户端的缓存就占满了）

缺点：体验不好、不灵活

方案二、智能判断如何收完（不能判断收空！）
服务端先发数据的长度（以此客户端来判断是否收完）


头部长度 头部数据  数据
"""