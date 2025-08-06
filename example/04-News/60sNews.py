# -*-coding:utf-8 -*-

"""
# File:         60sNews.py
# Time:         2025/8/6 15:56
# Author:       Martin
# Description:  
"""

import requests

url = "https://60s.viki.moe/v2/60s?date"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.json()['data'])