# -*-coding:utf-8 -*-

"""
# File: 03-os模块.py
# Time: 2025/9/21 19:39
# Author:   Martin
# Description:  
"""
import os

files = [
  '七龙珠.mp4',
  '海贼王海报.jpg',
  '90后回忆动画',
  '美少女战士.mp4',
  '数码宝贝主题曲.mp3',
  '犬夜叉片尾曲.mp3',
  '剧照',
  '火影忍者海报.jpg'
]

# 请补全代码
# listh_file = [os.path.splitext(i)[1] for i in files]
# extensions = [i for i in listh_file if i != '']
# extensions = list(set(extensions))
# print(extensions)
#

# 打印当前路径
print(os.getcwd())