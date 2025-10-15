# -*- coding: utf-8 -*-
"""
@File    : 28-asyncio标准款.py
@Author  : Martin
@Time    : 2025/10/13 18:03
@Desc    : 异步IO
"""
import asyncio


"""
事件循环
自动检测并执行我们添加给它的任务

任务列表 = [任务a,任务b....]
while True:
    可执行任务列表,已完成任务列表  = 检测任务列表
    for 任务 in 可执行任务列表:
        执行任务
    
    for 已完成任务 in 已完成任务列表:
        移除任务
    
    
    终止时间循环

asyncio.get_event_loop()
"""
from threading import current_thread

@asyncio.coroutine
def f1():
    print("f1 start", current_thread())
    yield from asyncio.sleep(1)


loop = asyncio.get_event_loop()

