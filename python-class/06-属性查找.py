# -*- coding: utf-8 -*-
"""
@File    : 06-属性查找.py
@Author  : Martin
@Time    : 2025/10/15 22:17
@Desc    :
属性查找基于：MRO列表！
"""
# 1继承查找

# class Test1:
#     def f1(self):
#         print('Test1.f1')
#
#     def f2(self):
#         print('Test1.f2')
#         self.f1()
#
#
# class Test2(Test1):
#     def f1(self):
#         print('Test2.f1')
#
#
# obj = Test2()
# obj.f2()
"""
Test1.f2
Test2.f1

注意：self ---> obj(对象)  self.f1()  --> obj.f1()
"""


# 多继承属性查找
# 2菱形问题（钻石问题）

# 继承顺序：MRO列表、C3算法实现的
class A:
    def f1(self):
        print('A.f1')


class B(A):
    def f1(self):
        print('B.f1')


class C(A):
    def f1(self):
        print('C.f1')


class D(B, C):
    def f2(self):
        print('D.f2')


print(D.mro())  # MRO列表、查找的顺序!!!!!!!
# [<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
obj = D()
obj.f1()  # B.f1

# 3.非菱形继承 （按顺序、先找第一个分支、找第一个分支的父类...,第二个分支....,最后才找object类

# 菱形继承
# 经典类：深度优先查找
# 新式类：广度优先查找