# -*-coding:utf-8 -*-

"""
# File:         calculator.py
# Time:         2025/8/5 12:59
# Author:       Martin
# Description:  计算器（eval的环境处理、避免黑客利用）
"""
from types import NoneType

while True:
    g = {}
    g['__builtins__'] = None
    try:
        res = eval(input('>>> '), g)
        print(res)
    except TypeError as e:
        print("请输入正确的数学表达式！")


