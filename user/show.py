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

# 解决中文显示问题
mpl.rcParams[u'font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False

class Show(object):
    def __init__(self, data=None, code='', path='./stocks/', freq = 'D', name = ''):
        signal.signal(signal.SIGINT, self.signal_handler)
        # print(data)
        # print(path)
        if path == '':
            self.path = './'
        else:
            self.path = path + '/'

        self.name = name
        self.code = code
        date = 2
        close = 6
        if freq != 'D':
            close = 3
        csv_data = pd.read_csv(self.path + self.code, usecols=[date, close], header=None)  # 读取数据
        self.data = csv_data.values.tolist()
        self.freq = freq

        self.colors = {'ma5':'gold', 'ma10':'pink', 'ma20': 'blueviolet', 'ma60':'cyan'}

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
        y = [round(i,2) for i in y]
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
            plt.scatter(high_x[i], high_y[i], s=25, color='red')      # s 为点的 size
            plt.annotate(str(high_y[i]), color='red', xy=(high_x[i], high_y[i]+0.003*high_y[i]), fontsize=10, xycoords='data')      # 在(3.3, 5.5)上做标注

        # 绘制散点(3, 6)
        for i in range(len(low_y)):
            plt.scatter(low_x[i], low_y[i], s=25, color='green')      # s 为点的 size
            plt.annotate(str(low_y[i]), color='green', xy=(low_x[i], low_y[i]-0.007*low_y[i]), fontsize=10, xycoords='data')      # 在(3.3, 5.5)上做标注

        # plt.text(3.3, 5, "this point very important",
        #     fontdict={'size': 12, 'color': 'green'})  # xycoords='data' 是说基于数据的值来选位置

    def draw_high_line(self, high_x, high_y):
        plt.plot(high_x, high_y, color='red', linewidth=1.0, linestyle="--", label="y")
        x = high_x
        y = high_y
        linewidth = 1.0
        while len(y) >= 2:
            high_x, high_y, temp_x, temp_y = self.get_point(x, y)
            x = high_x
            y = high_y
            linewidth += 0.75
            plt.plot(x, y, color='red', linewidth=linewidth, linestyle="--", label="y")

    def draw_low_line(self, low_x, low_y):
        plt.plot(low_x, low_y, color='green', linewidth=1.0, linestyle="--", label="y")
        x = low_x
        y = low_y
        linewidth = 1.0
        while len(x) >= 2:
            temp_x, temp_y, low_x, low_y = self.get_point(x, y)
            x = low_x
            y = low_y
            linewidth += 0.75
            plt.plot(x, y, color='green', linewidth=linewidth, linestyle="--", label="y")

    def get_average(self, price, number):
        average = []
        index = 0
        for i in range(len(price)):
            if i < number:
                index = 0
            else :
                index = i-(number-1)
            p = price[index:i+1]
            average.append(np.mean(p))
        return average

    def average_line(self, xs, ys):
        ma5 = self.get_average(ys, 5)
        ma10 = self.get_average(ys, 10)
        ma20 = self.get_average(ys, 20)
        # ma60 = self.get_average(ys, 60)

        pre_rush = False
        rush = False
        pre_run = False
        run = False

        ret = False
        for i in range(0, len(ys)):
            # rush
            if ma5[i] >= ma10[i]:
                if pre_rush == False:
                    pre_rush = True
                    code = self.code + ':'
                    if (xs[-1] - xs[i]).days < 3:
                        print(code, self.name, xs[i], 'pre_rush!')
                if ma10[i] >= ma20[i]:
                    if rush == False:
                        rush = True
                        code = self.code + ':'
                        plt.scatter(xs[i], ys[i], s=50, color='red')      # s 为点的 size
                        if (xs[-1] - xs[i]).days < 2:
                            print(code, self.name, xs[i], 'rush!!!')
                            ret = True

            if ma10[i] < ma20[i]:
                rush = False
            if ma5[i] < ma10[i]:
                if rush == False:
                    pre_rush = False
            # run
            # if ma5[i] <= ma10[i]:
            #     if pre_run == False:
            #         pre_run = True
            #         code = self.code + ':'
            #         print(code, xs[i], 'pre_run!')
            #     if ma10[i] <= ma20[i]:
            #         if run == False:
            #             run = True
            #             code = self.code + ':'
            #             plt.scatter(xs[i], ys[i], s=50, color='green')      # s 为点的 size
            #             print(code, xs[i], 'run!!!')

            # if ma10[i] > ma20[i]:
            #     run = False
            # if ma5[i] > ma10[i]:
            #     if run == False:
            #         pre_run = False
        plt.plot(xs, ma5, color=self.colors['ma5'], linewidth=1.5, linestyle="-", label='ma5')
        plt.plot(xs, ma10, color=self.colors['ma10'], linewidth=1.5, linestyle="-", label='ma10')
        plt.plot(xs, ma20, color=self.colors['ma20'], linewidth=1.5, linestyle="-", label='ma20')
        # plt.plot(xs, ma60, color=self.colors['ma60'], linewidth=1.5, linestyle="-", label='ma60')
        return ret

    def show(self):
        # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
        plt.figure(figsize=(24, 13.5), dpi=80)
        # 再创建一个规格为 1 x 1 的子图
        plt.subplot(111)
        # fig1, ax = plt.subplots()
        plt.title(self.name)

        xs, ys = self.get_position()

        flag = self.average_line(xs, ys)
        high_x, high_y, low_x, low_y = self.get_point(xs, ys)
        self.draw_point(high_x, high_y, low_x, low_y)
        # self.draw_high_line(high_x, high_y)
        # self.draw_low_line(low_x, low_y)

        plt.plot(xs, ys, color='blue', linewidth=1.0, linestyle="-", label="price")
        plt.legend(loc='upper left',ncol=2)   # 图例

        # 设置横轴的上下限
        # plt.xlim(20160818, 20200901)
        # 设置纵轴的上下限
        # plt.ylim(30, 500)
        # 设置横轴标签
        plt.xlabel("X")
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
        if flag is True:
            plt.savefig(self.path + self.code + '_' + self.name+ '.png')

        # plt.show(block=False)
        # while plt.waitforbuttonpress() == False:
        #     time.sleep(0.1)

if __name__ == "__main__":
    csv_file = sys.argv[1]
    freq = 'D'
    name = ''
    path = './stocks/'

    if len(sys.argv) == 5:
        path = sys.argv[4]
        freq = sys.argv[3]
        name = sys.argv[2]
    elif len(sys.argv) == 4:
        freq = sys.argv[3]
        name = sys.argv[2]
    elif len(sys.argv) == 3:
        name = sys.argv[2]

    show = Show(code = csv_file, name = name, freq=freq, path=path)
    show.show()


