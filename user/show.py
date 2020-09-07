#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import signal
import time
from datetime import datetime
import cv2 as cv
import pandas as pd
import matplotlib.pyplot as plt   # 导入模块 matplotlib.pyplot，并简写成 plt
import numpy as np                # 导入模块 numpy，并简写成 np

class Show(object):
    def __init__(self, data=None, name='', path='', freq = 'D'):
        signal.signal(signal.SIGINT, self.signal_handler)
        # print(data)
        print(path)
        if path == '':
            self.path = './'
        else:
            self.path = path + '/'

        self.name = name
        date = 2
        close = 6
        if freq != 'D':
            close = 3
        csv_data = pd.read_csv(self.path + self.name, usecols=[date, close], header=None)  # 读取数据
        self.data = csv_data.values.tolist()
        self.freq = freq

    def signal_handler(self, signal, frame):
        sys.exit(0)

    def get_position(self):
        x = [i[0] for i in self.data]
        x.reverse()
        # print(x)
        # print(len(x))
        xs = [datetime.strptime(str(d)[0:-2], '%Y%m%d').date() for d in x]
        # print(xs)
        y = [i[1] for i in self.data]
        y.reverse()
        # print(y)
        return xs, y

    def get_point(self, xs, y):
        price_last = 0
        price = 0
        high_x = []
        high_y = []
        low_x = []
        low_y = []
        for i in range(len(y)):
            if i == 1:
                if price >= y[i]:
                    high_x.append(xs[i-1])
                    high_y.append(price)
                elif price <= y[i]:
                    low_x.append(xs[i-1])
                    low_y.append(price)

            if i == len(y) - 1:
                if price <= y[i]:
                    high_x.append(xs[i])
                    high_y.append(y[i])
                elif price >= y[i]:
                    low_x.append(xs[i])
                    low_y.append(y[i])

            if price >= y[i] and price >= price_last and price_last != 0:
                high_x.append(xs[i-1])
                high_y.append(price)

            if price <= y[i] and price <= price_last and price_last != 0:
                low_x.append(xs[i-1])
                low_y.append(price)

            price_last = price
            price = y[i]
        return high_x, high_y, low_x, low_y

    def draw_point(self, high_x, high_y, low_x, low_y):
        # 绘制散点(3, 6)
        for i in range(len(high_y)):
            plt.scatter(high_x[i], high_y[i], s=30, color='red')      # s 为点的 size
            # 对(3, 6)做标注
            plt.annotate(str(high_y[i]), xy=(high_x[i], high_y[i]+0.5), fontsize=10, xycoords='data')      # 在(3.3, 5.5)上做标注

        # 绘制散点(3, 6)
        for i in range(len(low_y)):
            plt.scatter(low_x[i], low_y[i], s=30, color='green')      # s 为点的 size
            # 对(3, 6)做标注
            plt.annotate(str(low_y[i]), xy=(low_x[i], low_y[i]-3.5), fontsize=10, xycoords='data')      # 在(3.3, 5.5)上做标注

        # plt.text(3.3, 5, "this point very important",
        #     fontdict={'size': 12, 'color': 'green'})  # xycoords='data' 是说基于数据的值来选位置

    def draw_high_line(self, high_x, high_y):
        x = high_x
        y = high_y
        linewidth = 1.0
        while len(y) >= 2:
            high_x, high_y, temp_x, temp_y = self.get_point(x, y)
            x = high_x
            y = high_y
            linewidth += 0.5
            plt.plot(x, y, color='red', linewidth=linewidth, linestyle="--", label="y")

    def draw_low_line(self, low_x, low_y):
        x = low_x
        y = low_y
        linewidth = 1.0
        while len(x) >= 2:
            temp_x, temp_y, low_x, low_y = self.get_point(x, y)
            x = low_x
            y = low_y
            linewidth += 0.5
            plt.plot(x, y, color='green', linewidth=linewidth, linestyle="--", label="y")
    def show(self):
        # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
        # plt.figure(figsize=(16, 9), dpi=80)
        # 再创建一个规格为 1 x 1 的子图
        # plt.subplot(111)
        fig1, ax = plt.subplots()
        plt.title(self.name)

        xs, ys = self.get_position()
        high_x, high_y, low_x, low_y = self.get_point(xs, ys)
        self.draw_point(high_x, high_y, low_x, low_y)
        self.draw_high_line(high_x, high_y)
        self.draw_low_line(low_x, low_y)

        plt.plot(high_x, high_y, color='red', linewidth=1.0, linestyle="--", label="y")
        plt.plot(low_x, low_y, color='green', linewidth=1.0, linestyle="--", label="y")
        # 绘制颜色为蓝色、宽度为 1 像素的连续曲线 y1
        plt.plot(xs, ys, 'b', linewidth=1.0, linestyle="-", label="y")
        # plt.gcf().autofmt_xdate()

        # plt.legend(loc="upper left")
        # 设置横轴的上下限
        # plt.xlim(20160818, 20200901)
        # 设置纵轴的上下限
        # plt.ylim(30, 500)
        # 设置横轴标签
        # plt.xlabel("X")
        # 设置纵轴标签
        # plt.ylabel("Y")
        # 设置横轴精准刻度
        # plt.xticks([-1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5])
        # 设置纵轴精准刻度
        # plt.yticks([-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        # 设置横轴精准刻度
        xticks=list(range(0,len(xs),5))
        xlabels=[xs[x] for x in xticks]
        xlabels.append(xs[-1])
        plt.xticks(xlabels, rotation = -90)
        # # 设置纵轴精准刻度
        # plt.yticks([-2, 0, 2, 4, 6, 8, 10],
        #         ["-2m", "0m", "2m", "4m", "6m", "8m", "10m"])
        plt.show(block=False)
        while plt.waitforbuttonpress() == False:
            time.sleep(0.1)

        plt.savefig(self.path + self.name + '.jpg')
if __name__ == "__main__":

    csv_file = sys.argv[1]
    # print('csv_file:', csv_file)

    # csv_data = pd.read_csv(csv_file, usecols=[2,6])  # 读取数据
    # print(csv_data.shape)  # (189, 9)
    # print(csv_data.head(5))  # (189, 9)
    # N = 5
    # csv_batch_data = csv_data.tail(N)  # 取后5条数据
    # print('csv_batch_data:',csv_batch_data)
    # print(csv_batch_data.shape)  # (5, 9)

    # train_batch_data = csv_data.ix[:,:]#[list(range(3, 6))]  # 取这20条数据的3到5列值(索引从0开始)
    # print(train_batch_data)

    # exit(0)
    show = Show(name = csv_file)
    show.show()


