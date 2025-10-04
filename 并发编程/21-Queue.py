# -*- coding: utf-8 -*-
"""
@File    : 21-Queue.py
@Author  : Martin
@Time    : 2025/10/4 13:21
@Desc    : 
"""
import queue
q = queue.Queue()
q.put(1)
q.get()
q.full()
q.get_nowait()
q.put_nowait(1)

# 优先级队列
q1 = queue.PriorityQueue()
q.put((12,"a"))
q.put((-1,"a"))
q.put((69,"a"))
q.get_nowait()
# 后进先出队列（堆栈）
q2 = queue.LifoQueue()
q.put(1)
q.get()
q.full()
q.get_nowait()
q.put_nowait(1)