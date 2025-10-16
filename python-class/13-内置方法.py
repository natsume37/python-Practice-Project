# -*- coding: utf-8 -*-
"""
@File    : 13-内置方法.py
@Author  : Martin
@Time    : 2025/10/16 21:39
@Desc    : 
"""
l = [1, 2, 3]
print(l)  # [1, 2, 3]


# 如何实现我们自己定义的对象支持print函数呢？
class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 在特殊情况自动触发（print的时候)
    def __str__(self):
        # 注意返回的是字符串类型
        return f'{self.name} {self.age}'

    def __del__(self):
        print('__del__运行了')


obj = Human('Martin', 18)
# print(obj)

# __del__()  ：程序的最后一行代码执行完毕后开始删除对象 （垃圾回收的时候执行）
# 在删除对象的时候先执行
"""
应用场景：当对象调用操作系统资源后、可以在对象被删除之前高数操作系统关闭资源
"""
# 通过验证 __del__()在程序运行结束之后执行了
print('='*50)