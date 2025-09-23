# -*-coding:utf-8 -*-

"""
# File: 01-服务端.py
# Time: 2025/9/22 17:19
# Author:   Martin
# Description:  TCP并发编程Demo
"""
import socketserver

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.request)
        print(self.client_address)
        while True:
            try:  # 异常断开、windows直接报错问题
                data = self.request.recv(1024)
            except:
                break
            if not data:  # mac/linux解决异常断开收空问题
                break
            data = data.decode("utf-8")
            print('客户端数据：', data)
            self.request.send(data.upper().encode('utf-8'))
        self.request.close()

# windows系统只能调用线程
# 进厂原理
# import os
# os.fork() # 只支持mac\linux

sk = socketserver.ThreadingTCPServer(('127.0.0.1', 8088),RequestHandler)
sk.serve_forever()

# while True:
#     conn,addr = sk.accept()
# 起一个线程、实例化Requesthandle、继续服务下一个




