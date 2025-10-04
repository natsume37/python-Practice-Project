# -*- coding: utf-8 -*-
"""
@File    : 24-回调机制.py
@Author  : Martin
@Time    : 2025/10/4 14:08
@Desc    : 回调机制
异步任务执行完毕后、会将返回结果传给回到函数进行处理
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

# pool = ThreadPoolExecutor()  # 目前默认CPU个数加4
pool = ProcessPoolExecutor()  # 目前默认CPU个数加4


def task(name):
    print(name)
    time.sleep(3)
    return name + 10


def call_back(res):
    print(f"coll_back:{res.result()}")


if __name__ == '__main__':
    # f_list = []
    for i in range(50):
        future = pool.submit(task, i).add_done_callback(call_back)  # 增加回调机制：异步任务执行完毕后、会将返回结果传给回到函数进行处理
        # f_list.append(future)

    pool.shutdown()  # 关闭线程池、等待线程池中的线程全部执行完毕

    # 将异步提交的结果全部放到列表里然后同步打印
    # for f in f_list:
    #     print(f"任务结果：{f.result()}")
