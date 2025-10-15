# -*- coding: utf-8 -*-
"""
@File    : 03-类装饰器.py
@Author  : Martin
@Time    : 2025/10/13 13:46
@Desc    : 
"""


class Test:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def set_age(self, new_age):
        if type(new_age) is not int:
            print("你个傻子、要整数类型！")
            return
        if new_age <0:
            print("小老弟、不太对劲")
            return
        self.__age = new_age
    def del_age(self):
        del self.__age

obj = Test("Martin", 18)
# print(obj.get_age())  # 不符合使用逻辑  (obj.age   obj.name)
# print(obj.get_name())
