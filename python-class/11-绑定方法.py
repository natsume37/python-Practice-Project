# -*- coding: utf-8 -*-
"""
@File    : 11-绑定方法.py
@Author  : Martin
@Time    : 2025/10/16 11:11
@Desc    : 
"""
from traceback import print_tb

import setting


# 案例

class Mysql:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def f1(self):
        print(self.ip, self.port)

    @staticmethod  # 非绑定方法：静态方法 --> 普通函数
    def f2():
        print("嘿嘿嘿嘿")

    @classmethod  # 绑定给类的方法、类调用的话、自动传入类对象
    def instance_from_conf(cls):
        print(cls)
        # obj = Mysql(setting.IP, setting.PORT)
        obj1 = cls(setting.IP, setting.PORT)
        return obj1


obj = Mysql.instance_from_conf()
print(obj.__dict__)
"""
<class '__main__.Mysql'>
{'ip': '127.0.0.1', 'port': 8080}
"""
