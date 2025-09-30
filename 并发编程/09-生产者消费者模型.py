# -*- coding: utf-8 -*-
"""
@File    : 09-生产者消费者模型.py
@Author  : Martin
@Time    : 2025/9/30 21:17
@Desc    : JoinableQueue
生产者：生成或制造数据的
消费者：消费或处理数据党的
媒介：消息队列

"""
# from multiprocessing import Process, Queue
# import time
# import random
#
#
# def producer(name, food, q):
#     for i in range(8):
#         time.sleep(random.randint(1, 3))
#         print(f"{name}做了{food}")
#         q.put(f"{food}{i}")
#
#
# def consumer(name, q):
#     while True:
#         food = q.get()
#         time.sleep(random.randint(1, 3))
#         print(f"{name}吃了{food}")
#         if food == "鹤顶红":
#             break
#
#
# if __name__ == '__main__':
#     q = Queue()
#     p1 = Process(target=producer, args=("Martin", "黄金蛋炒饭", q))
#     p2 = Process(target=producer, args=("神厨小福贵", "佛跳墙", q))
#     c1 = Process(target=consumer, args=("八戒", q))
#     c2 = Process(target=consumer, args=("悟空", q))
#     p1.start()
#     p2.start()
#     c1.start()
#     c2.start()
#
#     # 等待生产者全部生产完、然后准备结束
#     p1.join()
#     p2.join()
#     q.put("鹤顶红")
#     # 因为有两个消费者所以要加两个毒
#     q.put("鹤顶红")


# 统计消费者、智能添加鹤顶红
# from multiprocessing import Process, Queue
# import time
# import random
# from multiprocessing.dummy import JoinableQueue
#
#
# # 定义元类
# class CountMeta(type):
#     _count = 0
#
#     def __call__(cls, *args, **kwargs):
#         # 每实例化一次，就加 1
#         CountMeta._count += 1
#         return super().__call__(*args, **kwargs)
#
#     @classmethod
#     def get_count(mcls):
#         return mcls._count
#
#
# # 定义一个使用元类的 Process 子类
# class MyProcess(Process, metaclass=CountMeta):
#     pass
#
#
# def producer(name, food, q):
#     for i in range(8):
#         time.sleep(random.randint(1, 3))
#         print(f"{name}做了{food}")
#         q.put(f"{food}{i}")
#
#
# def consumer(name, q):
#     while True:
#         food = q.get()
#         time.sleep(random.randint(1, 3))
#         print(f"{name}吃了{food}")
#         if food == "鹤顶红":
#             break
#
#
# if __name__ == '__main__':
#     q = JoinableQueue()
#     p1 = MyProcess(target=producer, args=("Martin", "黄金蛋炒饭", q))
#     p2 = MyProcess(target=producer, args=("神厨小福贵", "佛跳墙", q))
#     c1 = Process(target=consumer, args=("八戒", q))
#     c2 = Process(target=consumer, args=("悟空", q))
#     p1.start()
#     p2.start()
#     c1.start()
#     c2.start()
#     p1.join()
#     p2.join()

# JoinableQueue
from multiprocessing import Process, Queue, JoinableQueue
import time
import random

"""
JoinableQueue 在queue的基础上多了个计数器机制、没put一个数据、计数器+1
调用一次task_done()计数器-1
计数器为0时、走q.join()后的代码
"""


def producer(name, food, q):
    for i in range(8):
        time.sleep(random.randint(1, 3))
        print(f"{name}做了{food}")
        q.put(f"{food}{i}")


def consumer(name, q):
    while True:
        food = q.get()
        time.sleep(random.randint(1, 3))
        print(f"{name}吃了{food}")
        # if food == "鹤顶红":
        #     break
        q.task_done()  # 告诉队列、已经拿走了一个数据且已经处理完了


if __name__ == '__main__':
    q = JoinableQueue()
    p1 = Process(target=producer, args=("Martin", "黄金蛋炒饭", q))
    p2 = Process(target=producer, args=("神厨小福贵", "佛跳墙", q))
    c1 = Process(target=consumer, args=("八戒", q))
    c2 = Process(target=consumer, args=("悟空", q))
    p1.start()
    p2.start()

    # 设置守护进程、保证子进程死掉
    c1.daemon = True
    c2.daemon = True

    c1.start()
    c2.start()

    # 等待生产者全部生产完、然后准备结束
    p1.join()
    p2.join()

    q.join()
    # 主进程死了、消费者也要死掉（守护进程）
