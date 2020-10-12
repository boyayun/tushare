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


l = {
    # 'amount0': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  'amount1': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  'amount2': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'rsi6_12': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  'rsi1224': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ma4___9': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ma9__18': [0, 0, 0, 0, 0, 0, 0, 0, 0]}

if os.path.exists('./statistics.csv'):
    csv_data = pd.read_csv('./statistics.csv', header=None)  # 读取数据
    data = csv_data.values.tolist()
    for i in data:
        code = i[0]
        name = i[1]
        tag = i[2]
        l[tag][0] += 1
        k = 0
        for j in range(1, 9-k):
            if i[4+k] < i[4+j+k]:
                l[tag][j+k] += 1

    print(l)
    for (key, value) in l.items():
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
