# -*-coding:utf-8 -*-

"""
# File:         石头剪刀布.py
# Time:         2025/8/5 10:07
# Author:       Martin
# Description:  
"""
import random

def play():
    options = ['石头', '剪刀', '布']
    outcomes = {
        ('石头', '剪刀'): '你赢了！',
        ('剪刀', '布'): '你赢了！',
        ('布', '石头'): '你赢了！'
    }
    while True:
        user = input('请输入（剪刀or石头or布）')
        if user not in options:
            print('请输入合法的内容')
            continue
        comp = random.choice(options)
        print(f'你出的是：{user},电脑出的是：{comp}')
        if user == comp:
            print('平局')
        else:
            print(outcomes.get((user, comp),'你输了'))
        answer = input('再来一局？（Y/N）：').strip().lower()
        if answer not in ('', 'y'):
            break

if __name__ == '__main__':
    play()





