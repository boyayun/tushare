#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import signal
import time
from datetime import datetime
from datetime import timedelta
# import cv2 as cv
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt   # 导入模块 matplotlib.pyplot，并简写成 plt
import numpy as np                # 导入模块 numpy，并简写成 np
import csv


l_rush = {
    # 'amount0': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    # 'amount1': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    # 'amount2': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'test': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'price__': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'rsi6_12': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ma4___9': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ma9__18': [0, 0, 0, 0, 0, 0, 0, 0, 0]}

l_run = {
    # 'amount0': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    # 'amount1': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    # 'amount2': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'test': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'price__': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'rsi6_12': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ma4___9': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ma9__18': [0, 0, 0, 0, 0, 0, 0, 0, 0]}

if os.path.exists('./statistics.csv'):
    csv_data = pd.read_csv('./statistics.csv', header=None)  # 读取数据
    data = csv_data.values.tolist()
    name = 'init'
    price = 100
    hold = False
    buy = 1
    sell = 1
    number = -1
    total = -100
    for i in data:
        code = i[0]
        tag = i[2]
        if i[3] == 'run':
            k = 0
            l_run[tag][0] += 1
            for j in range(1, 9-k):
                if i[5+k] > i[5+j+k]:
                    l_run[tag][j+k] += 1
        elif i[3] == 'rush':
            k = 0
            l_rush[tag][0] += 1
            for j in range(1, 9-k):
                if i[5+k] < i[5+k+j]:
                    l_rush[tag][j+k] += 1

        # print(i[1])
        if i[1] != name:
            print('name:', name, round(price, 2))
            number += 1
            name = i[1]
            total += price
            price = 100
            hold = False

        if i[2] == 'ma9__18':
            if i[3] == 'rush' and hold == False:
                hold = True
                buy = i[6]
            if i[3] == 'run' and hold == True:
                hold = False
                sell = i[6]
                price = price*sell/buy
                # print('name:', name, round(price, 2))
    print('name:', name, round(price, 2))
    total += price
    number += 1
    print('total:', round(total, 2), number, round(total/number, 2))
    # exit(0)

    print('rush', l_rush)
    for (key, value) in l_rush.items():
        if value[0] != 0:
            v1 = value[1]/value[0]*100
            v2 = value[2]/value[0]*100
            v3 = value[3]/value[0]*100
            v4 = value[4]/value[0]*100
            v5 = value[5]/value[0]*100
            v10 = value[6]/value[0]*100
            v20 = value[7]/value[0]*100
            v30 = value[8]/value[0]*100
            print('%s:1day:%.2f%%,2day:%.2f%%,3day:%.2f%%,4day:%.2f%%,5day:%.2f%%,10day:%.2f%%,20day:%.2f%%,30day:%.2f%%' % (
                key, v1, v2, v3, v4, v5, v10, v20, v30))

    print('\nrun', l_run)
    for (key, value) in l_run.items():
        if value[0] != 0:
            v1 = value[1]/value[0]*100
            v2 = value[2]/value[0]*100
            v3 = value[3]/value[0]*100
            v4 = value[4]/value[0]*100
            v5 = value[5]/value[0]*100
            v10 = value[6]/value[0]*100
            v20 = value[7]/value[0]*100
            v30 = value[8]/value[0]*100
            print('%s:1day:%.2f%%,2day:%.2f%%,3day:%.2f%%,4day:%.2f%%,5day:%.2f%%,10day:%.2f%%,20day:%.2f%%,30day:%.2f%%' % (
                key, v1, v2, v3, v4, v5, v10, v20, v30))
