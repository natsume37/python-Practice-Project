# -*- coding: utf-8 -*-
"""
@File    : 07-消息队列.py
@Author  : Martin
@Time    : 2025/9/30 20:55
@Desc    : 队列： 先进先出  管道+锁
            堆栈：先进后出
"""
# import queue
#
# queue.Queue()
from multiprocessing import Queue

q = Queue(6)  # 有默认大小
q.put("a")
q.put("b")
q.put("c")
q.put("d")
q.put("e")
q.put("e")
q.full()  # 判断队列是否已满？bool
# q.put("f",timeout=3)
# q.put_nowait("f") # 不等待、直接报错
# q.put("g")  # 多存会阻塞
v1 = q.get()
v2 = q.get()
v3 = q.get()
v4 = q.get()
v5 = q.get()
v6 = q.get()
q.empty()  # 判断是否拿完？ 空
# v7 = q.get()
# v7 = q.get_nowait()
# v7 = q.get(timeout=3)
print(v1)

"""
q.put()
q.get()

# 以下方法多进程可能不准确
q.put_nowait()
q.get_nowait()
q.full()
q.empty()
"""
