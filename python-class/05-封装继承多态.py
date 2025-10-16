# -*- coding: utf-8 -*-
"""
@File    : 05-封装继承多态.py
@Author  : Martin
@Time    : 2025/10/15 21:40
@Desc    :
python3: 没有继承其他类、默认继承object类

继承：什么 ‘是’ 什么的关系
’is-a‘关系
"""

# 继承是创建新类的方式、 （子类、父类）
# object 兼容python2
# class Parent1(object):
#     pass
#
#
# class Parent2(object):
#     pass
#
#
# # 单继承
# class Child1(Parent1):
#     pass
#
#
# # 多继承
# class Child2(Parent1, Parent2):
#     pass
#
#
# print(Child1.__bases__)
# print(Child2.__bases__)
# print(Parent1.__bases__)  # (<class 'object'>,)
"""
(<class '__main__.Parent1'>,)
(<class '__main__.Parent1'>, <class '__main__.Parent2'>)
(<class 'object'>,)
"""

"""
python2中：新式类、和经典类
新式类：继承了object类的子类、以及继承了这个子类的子子孙孙类
经典类：没有继承object类的子类、以及继承了这个子类的子子孙孙类（默认类）
"""

# 继承的特性：遗传

# 多继承
# 优点：一个子类可以继承多个父类的属性
# 缺点：
# 1.不符合思维习惯
# 2.多继承让代码的可读性变差
# 如果必须用多继承、必须用Mixins-(编程规范）

# 派生 ：子类根据父类的属性或者自己创造属性
# 第一种情况：子类完全继承父类的属性、不需要修改
# class Human:
#     star = 'earth'
#
#     def __init__(self, name, age, gender):
#         self.name = name
#         self.age = age
#         self.gender = gender
#
#
# class Chinese(Human):
#     # star = 'earth'
#     nation = 'China'
#
#     # def __init__(self, name, age, gender):
#     #     self.name = name
#     #     self.age = age
#     #     self.gender = gender
#
#     def speak_chinese(self):
#         print(f'{self.name}在说普通话')
#
#
# class American(Human):
#     # star = 'earth'
#     nation = 'American'
#
#     # def __init__(self, name, age, gender):
#     #     self.name = name
#     #     self.age = age
#     #     self.gender = gender
#
#     def speak_english(self):
#         print(f'{self.name}speak english')
#
#
# dy_obj = Chinese('Marin', 18, "男")
# print(dy_obj.__dict__)
# print(dy_obj.nation)
# print(dy_obj.star)
# dy_obj.speak_chinese()
"""
{'name': 'Marin', 'age': 18, 'gender': '男'}
China
earth
Marin在说普通话
"""


class Human:
    star = 'earth'

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


class Chinese(Human):
    # star = 'earth'
    nation = 'China'

    def __init__(self, name, age, gender, balance):
        # self.name = name
        # self.age = age
        # self.gender = gender
        Human.__init__(self, name, age, gender)
        self.balance = balance

    def speak_chinese(self):
        print(f'{self.name}在说普通话')


class American(Human):
    # star = 'earth'
    nation = 'American'

    # def __init__(self, name, age, gender):
    #     self.name = name
    #     self.age = age
    #     self.gender = gender

    def speak_english(self):
        print(f'{self.name}speak english')


dy_obj = Chinese('Marin', 18, "男", 100)
print(dy_obj.__dict__)
print(dy_obj.nation)
print(dy_obj.star)
dy_obj.speak_chinese()


# 多态
# 汽车：奔驰、理想、小米、华为

class car:
    def run(self):
        print('run')


class xiaomi(car):
    def run(self):
        super().run()
        print('充电')


class lix(car):
    def run(self):
        super().run()
        print('换电')


car1 = xiaomi()


def driver_car(car):
    car.run()


driver_car(car1)

# 通过多态统一调用接口、不管是哪个类型、使用者的调用方法都是一样的
'123'.__len__()
[1, 2, 3].__len__()
{1: '1', 2: '2', 3: '3'}.__len__()


# 不同的类型有同样的方法名、就可以定义一个接口
def my_len(obj):
    return obj.__len__()


# len('123')
# len([1, 2, 3])
# len({1: '1', 2: '2'})

print(my_len('123'))
print(my_len([1, 2, 3]))
print(my_len({1: '1', 2: '2'}))

# __iter__
# for