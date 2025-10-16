# -*- coding: utf-8 -*-
"""
@File    : 14-元类.py
@Author  : Martin
@Time    : 2025/10/16 21:53
@Desc    :
class  做的事： Human = type(.......)
"""


# 模拟还原class 做的事情
class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        print(f'{self.name} is {self.age} years old.')


print(Human.__dict__)  # 有很多class帮我们创建的属性

# 1.类名
class_name = 'Human'

# 2.基类
class_base = (object,)
# 3.执行子列代码、产生命名空间
class_dic = {}

class_body = """
def __init__(self,name,age):
    self.name = name
    self.age = age
def info(self):
    print(self.name,self.age,self.name)
"""
# 第一个参数时子类代码、第二个参数是用到的全局命名空间
exec(class_body, {}, class_dic)
print(class_dic)  # 打印我们自定义的属性和方法

# 4.调用元类
# print(type(class_name, class_base, class_dic))

# 创建类对象 并给对象起名字
Human = type(class_name, class_base, class_dic)
obj = Human('Martin', 18)
print(obj.name)
print(obj.age)