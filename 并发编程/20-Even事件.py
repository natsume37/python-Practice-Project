# -*- coding: utf-8 -*-
"""
@File    : 20-Even事件.py
@Author  : Martin
@Time    : 2025/10/4 10:22
@Desc    : 
"""
from threading import Thread, Event
import time

event = Event()

def bus():
    print("公交车即将进站")
    time.sleep(3)
    event.set()
    print("公交车已到站")

def passenger(name):
    print(name,"wait")
    event.wait()
    print(name,"上车出发")

if __name__ == '__main__':
    t = Thread(target=bus)
    t.start()
    for i in range(10):
        t2 = Thread(target=passenger, args=(f"乘客{i+1}",))
        t2.start()