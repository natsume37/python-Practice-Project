# -*- coding: utf-8 -*-
"""
@File    : 01-类初识.py
@Author  : Martin
@Time    : 2025/10/12 16:36
@Desc    : 类就是容器：用于存放工具的容器（学其神而非形）
类的变量命名：驼峰体

python类的子代码在定义的时候就执行了
"""
class Hero:
    hero_work = "射手"
    def get_hero_info(self):
        print(self.hero_work)


print(Hero.__dict__)
print(Hero.__dict__['hero_work'])
