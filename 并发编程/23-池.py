# -*- coding: utf-8 -*-
"""
@File    : 23-池.py
@Author  : Martin
@Time    : 2025/10/4 13:42
@Desc    : 线程池、进程池
创建的进程池和线程池都是不会再变的（避免了进程线程的创建和销毁的资源浪费）
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

# pool = ThreadPoolExecutor()  # 目前默认CPU个数加4
pool = ProcessPoolExecutor()  # 目前默认CPU个数加4


def task(name):
    print(name)
    time.sleep(3)
    return name + 10

if __name__ == '__main__':
    f_list = []
    for i in range(50):
        # pool.submit(task,i) # 往线程池提交任务 异步提交
        # print("主线程")
        future = pool.submit(task, i)
        f_list.append(future)



    pool.shutdown() # 关闭线程池、等待线程池中的线程全部执行完毕

    # 将异步提交的结果全部放到列表里然后同步打印
    for f in f_list:
        print(f"任务结果：{f.result()}")
