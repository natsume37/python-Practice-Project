# -*- coding: utf-8 -*-
"""
@File    : 25-gevent初始.py
@Author  : Martin
@Time    : 2025/10/6 23:02
@Desc    : 
"""

# IO密集型
from gevent import monkey
monkey.patch_all()
from gevent import spawn
import time

# def da():
#     for _ in range(3):
#         print("哒")
#         time.sleep(2)
#
# def mie():
#     for _ in range(3):
#         print("咩")
#         time.sleep(2)
# start = time.time()
# da()
# mie()
# end = time.time()
# print(end - start)  # 12.00322937965393
#

def da():
    for _ in range(3):
        print("哒")
        time.sleep(2)

def mie():
    for _ in range(3):
        print("咩")
        time.sleep(2)
start = time.time()
g1 = spawn(da)
g2 = spawn(mie)
g1.join()
g2.join()
end = time.time()
print(end - start)