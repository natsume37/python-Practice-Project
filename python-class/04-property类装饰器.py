# -*- coding: utf-8 -*-
"""
@File    : 04-property类装饰器.py
@Author  : Martin
@Time    : 2025/10/13 13:54
@Desc    : 
"""


# class Test:
#     def __init__(self, name, age):
#         self.__name = name
#         self.__age = age
#
#     def get_name(self):
#         return self.__name
#
#     # @property  #get_age = property(get_age)
#     def get_age(self):
#         return self.__age
#
#     def set_age(self, new_age):
#         if type(new_age) is not int:
#             print("你个傻子、要整数类型！")
#             return
#         if new_age < 0:
#             print("小老弟、不太对劲")
#             return
#         self.__age = new_age
#
#     def del_age(self):
#         del self.__age
#
#     age = property(get_age, set_age, del_age)  # 顺序不能乱
#
#
# obj = Test("Martin", 18)
# # print(obj.get_age)  # 18
# print(obj.age)


# 语法糖版本
class Test:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def get_name(self):
        return self.__name

    @property  #get_age = property(get_age)
    def age(self):
        return self.__age
    @age.setter
    def age(self, new_age):
        if type(new_age) is not int:
            print("你个傻子、要整数类型！")
            return
        if new_age < 0:
            print("小老弟、不太对劲")
            return
        self.__age = new_age
    @age.deleter
    def age(self):
        del self.__age



obj = Test("Martin", 18)
# print(obj.get_age)  # 18
print(obj.age)
obj.age = 20
print(obj.age)
del obj.age