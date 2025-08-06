# -*-coding:utf-8 -*-

"""
# File:         01推导式.py
# Time:         2025/8/6 16:47
# Author:       Martin
# Description:  
"""

# 推导式（Syntactic sugar）是一种简洁的语法结构，它允许你通过一系列的操作来创建列表、集合或字典。

# 列表推导式
# 列表推导式是一种创建列表的简洁方式，它允许你根据一个表达式来创建列表。
# 语法：
# [expression for item in iterable if condition]
# 表达式：   表达式可以是任何有效的Python表达式，它会在每个迭代中计算一次。
# 项：       项可以是任何可迭代对象，如列表、元组、字符串等。
# 条件：     条件是一个可选的表达式，它会在每个迭代中进行计算，只有满足条件的项才会被包含在结果列表中。
# 示例：
# 1. 计算列表中的平方
squares = [x**2 for x in range(1, 11)]
print(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 2. 计算列表中的偶数
evens = [x for x in range(1, 11) if x % 2 == 0]
print(evens)  # [2, 4, 6, 8, 10]

# 集合推导式
# 集合推导式是一种创建集合的简洁方式，它与列表推导式类似，但结果是一个集合而不是列表。
# 语法：
# {expression for item in iterable if condition}
# 示例：
# 1. 计算集合中的平方
squares = {x**2 for x in range(1, 11)}
print(squares)  # {1, 4, 9, 16, 25, 36, 49, 64, 81, 100}

# 字典推导式
# 字典推导式是一种创建字典的简洁方式，它与列表推导式类似，但结果是一个字典而不是列表。
# 语法：
# {key_expression:value_expression for item in iterable if condition}
# 键表达式：  键表达式可以是任何有效的Python表达式，它会在每个迭代中计算一次，并作为字典的键。
# 值表达式：  值表达式可以是任何有效的Python表达式，它会在每个迭代中计算一次，并作为字典的值。
# 示例：
# 1. 计算字典中的键值对
squares = {x: x**2 for x in range(1, 11)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81, 10: 100}

# 元组推导式（生成器表达式）
# 元组推导式是一种创建元组的简洁方式，它与列表推导式类似，但结果是一个元组而不是列表。
# 语法：
# (expression for item in iterable if condition)
# 示例：
# 1. 计算元组中的平方
squares = tuple(x**2 for x in range(1, 11))  # 注意：tuple()函数用于将列表转换为元组

