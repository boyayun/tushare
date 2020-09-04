#!/usr/bin/python3
# -*- coding:utf-8 -*- 
import os
import sys
import signal
import time
import cv2 as cv

import matplotlib.pyplot as plt   # 导入模块 matplotlib.pyplot，并简写成 plt 
import numpy as np                # 导入模块 numpy，并简写成 np
    
class Show(object):
    def __init__(self, data=None, name=None, path=None):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.data = data
        self.name = name
        self.path = path

    def signal_handler(self, signal, frame):
        print('ctrl + c')
        sys.exit(0)

    def show(self):
        # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
        plt.figure(figsize=(8, 6), dpi=80)
        # 再创建一个规格为 1 x 1 的子图
        plt.subplot(111)

        x = np.linspace(-2, 6, 50)
        y1 = x + 3      # 曲线 y1
        y2 = 3 - x      # 曲线 y2


        # 绘制颜色为蓝色、宽度为 1 像素的连续曲线 y1
        plt.plot(x, y1, color="blue", linewidth=1.0, linestyle="-", label="y1")
        # 绘制散点(3, 6)
        plt.scatter([3], [6], s=30, color="blue")      # s 为点的 size
        # 对(3, 6)做标注
        plt.annotate("(3, 6)", xy=(3.3, 5.5))      # 在(3.3, 5.5)上做标注
        plt.text(3.3, 5, "this point very important",
            fontdict={'size': 12, 'color': 'green'})  # xycoords='data' 是说基于数据的值来选位置

        # 绘制颜色为红色、宽度为 2 像素的不连续曲线 y2
        plt.plot(x, y2, color="red", linewidth=2.0, linestyle="--", label="y2")
        # 绘制散点(3, 0)
        plt.scatter([3], [0], s=50, color="#800080")
        # 对(3, 0)做标注
        plt.annotate("(3, 0)",
                    xy=(3.3, 0),            # 在(3.3, 0)上做标注
                    fontsize=16,          # 设置字体大小为 16
                    xycoords='data')    # xycoords='data' 是说基于数据的值来选位置

        plt.legend(loc="upper left")
        
        # 设置横轴的上下限
        plt.xlim(-1, 6)
        # 设置纵轴的上下限
        plt.ylim(-2, 10)

        # 设置横轴标签
        plt.xlabel("X")
        # 设置纵轴标签
        plt.ylabel("Y")

        # 设置横轴精准刻度
        plt.xticks([-1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5])
        # 设置纵轴精准刻度
        plt.yticks([-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        # # 设置横轴精准刻度
        # plt.xticks([-1, 0, 1, 2, 3, 4, 5, 6],
        #         ["-1m", "0m", "1m", "2m", "3m", "4m", "5m", "6m"])
        # # 设置纵轴精准刻度
        # plt.yticks([-2, 0, 2, 4, 6, 8, 10],
        #         ["-2m", "0m", "2m", "4m", "6m", "8m", "10m"])
        plt.show(block=False)
if __name__ == "__main__":
    show = Show()
    show.show()
    while plt.waitforbuttonpress() == False:
        time.sleep(0.1)

    plt.savefig('testblueline.jpg')

