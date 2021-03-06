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

# 解决中文显示问题
mpl.matplotlib_fname()
mpl.rcParams[u'font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False

statistics = [[0 for row in range(0)] for col in range(14)]


class Show(object):
    def __init__(self, data=None, code='', path='./stocks/', freq='D', name=''):
        signal.signal(signal.SIGINT, self.signal_handler)
        if path == '':
            self.path = './'
        else:
            self.path = path + '/'

        self.name = name
        self.code = code
        csv_data = pd.read_csv(self.path + self.code + '_price_' +
                               freq + '.csv', usecols=[2, 3, 10], header=None)  # 读取数据
        self.data = csv_data.values.tolist()
        self.freq = freq

        self.colors = {'ma4': 'gold', 'ma9': 'pink',
                       'ma18': 'blueviolet', 'ma60': 'cyan'}

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
        y = [round(i, 2) for i in y]
        y.reverse()
        # print(y)
        amount = [i[2] for i in self.data]
        amount = [round(i, 2) for i in amount]
        amount.reverse()
        return xs, y, amount

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
            plt.scatter(high_x[i], high_y[i], s=25,
                        color='red')      # s 为点的 size
            plt.annotate(str(high_y[i]), color='red', xy=(
                high_x[i], high_y[i]+0.003*high_y[i]), fontsize=10, xycoords='data')      # 在(3.3, 5.5)上做标注

        # 绘制散点(3, 6)
        for i in range(len(low_y)):
            plt.scatter(low_x[i], low_y[i], s=25,
                        color='green')      # s 为点的 size
            plt.annotate(str(low_y[i]), color='green', xy=(
                low_x[i], low_y[i]-0.007*low_y[i]), fontsize=10, xycoords='data')      # 在(3.3, 5.5)上做标注

        # plt.text(3.3, 5, "this point very important",
        #     fontdict={'size': 12, 'color': 'green'})  # xycoords='data' 是说基于数据的值来选位置

    def draw_high_line(self, high_x, high_y):
        plt.plot(high_x, high_y, color='red',
                 linewidth=1.0, linestyle="--", label="y")
        x = high_x
        y = high_y
        linewidth = 1.0
        while len(y) >= 2:
            high_x, high_y, temp_x, temp_y = self.get_point(x, y)
            x = high_x
            y = high_y
            linewidth += 0.75
            plt.plot(x, y, color='red', linewidth=linewidth,
                     linestyle="--", label="y")

    def draw_low_line(self, low_x, low_y):
        plt.plot(low_x, low_y, color='green',
                 linewidth=1.0, linestyle="--", label="y")
        x = low_x
        y = low_y
        linewidth = 1.0
        while len(x) >= 2:
            temp_x, temp_y, low_x, low_y = self.get_point(x, y)
            x = low_x
            y = low_y
            linewidth += 0.75
            plt.plot(x, y, color='green', linewidth=linewidth,
                     linestyle="--", label="y")

    def get_statistics(self, xs, ys, index, tag, meta):
        if index+22 > len(ys)-1 or index < 22:
            return

        statistics[0].append(self.code)
        statistics[1].append(self.name)
        statistics[2].append(tag)
        statistics[3].append(meta)
        statistics[4].append(datetime.strftime(xs[index], "%Y%m%d"))
        statistics[5].append(ys[index])
        statistics[6].append(ys[index+1])
        statistics[7].append(ys[index+2])
        statistics[8].append(ys[index+3])
        statistics[9].append(ys[index+4])
        statistics[10].append(ys[index+5])
        statistics[11].append(ys[index+10])
        statistics[12].append(ys[index+15])
        statistics[13].append(ys[index+22])
        # print(statistics)

    def amount_price_select(self, xs, ys, amount):
        code = self.code + ':'
        for i in range(5, len(ys)):
            if(ys[i-4] < ys[i-5]) and amount[i-4] < amount[i-5]*0.9:
                if(ys[i-3] < ys[i-4]) and amount[i-3] < amount[i-4]*0.9:
                    if(ys[i-2] < ys[i-3]) and amount[i-2] < amount[i-3]*0.9:
                        # self.get_statistics(xs, ys, i, 'amount0')
                        if(ys[i-1] < ys[i-2]) and amount[i-1] < amount[i-2]*0.9:
                            # self.get_statistics(xs, ys, i, 'amount1')
                            if(ys[i] > ys[i-1]) and amount[i] > amount[i-1]*1.2:
                                # self.get_statistics(xs, ys, i, 'amount2')
                                if (len(ys) - i - 1) < 2:
                                    print(code, self.name,
                                          xs[i], 'amount_price rush!!!')

    def price_select(self, xs, ys):
        code = self.code + ':'
        max = 0
        rush = False
        rsi6 = self.get_rsi(ys, 6)
        rsi12 = self.get_rsi(ys, 12)

        for i in range(0, len(ys)):
            if ys[i] >= max:
                max = ys[i]
            #     if rush == False:
            #         rush = True
            #         self.get_statistics(xs, ys, i, 'price__', 'rush')
            #         if (len(ys) - i - 1) < 2:
            #             print(code, self.name, xs[i], 'price rush!!!')
            if rsi6[i] > rsi12[i]:
                if rush == False and rsi12[i] < 40 and rsi12[i] > 30:
                    rush = True
                    self.get_statistics(xs, ys, i, 'test', 'rush')
                    max = ys[i]
                    if (len(ys) - i - 1) < 2:
                        print(code, self.name, xs[i], 'rsi rush!!!')

            if ys[i] < max*0.95 and rush == True:
                rush = False
                self.get_statistics(xs, ys, i, 'test', 'run')
                if (len(ys) - i - 1) < 2:
                    print(code, self.name, xs[i], 'test run!!!')

    def get_smooth(self, price, number):
        smooth = [0]
        for i in range(1, len(price)):
            p = price[i]/number+smooth[i-1]*(number-1)/number
            smooth.append(p)
        return smooth

    def get_rsi(self, price, number):
        rsi = [0]
        up = [0]
        down = [0]
        for i in range(1, len(price)):
            temp = price[i] - price[i-1]
            if temp >= 0:
                up.append(temp)
                down.append(0)
            else:
                down.append(abs(temp))
                up.append(0)

        up_smooth = self.get_smooth(up, number)
        down_smooth = self.get_smooth(down, number)

        for i in range(1, len(price)):
            if up_smooth[i] == 0 and down_smooth[i] == 0:
                r = rsi[i-1]
            else:
                r = up_smooth[i]/(up_smooth[i]+down_smooth[i])*100
            rsi.append(round(r, 2))
        return rsi

    def rsi_select(self, xs, ys):
        code = self.code + ':'

        rsi6 = self.get_rsi(ys, 6)
        rsi12 = self.get_rsi(ys, 12)
        # rsi24 = self.get_rsi(ys, 24)

        rush = False
        run = False

        for i in range(0, len(ys)):
            if rsi6[i] > rsi12[i]:
                run = False
                if rush == False and rsi12[i] < 40 and rsi12[i] > 30:
                    rush = True
                    self.get_statistics(xs, ys, i, 'rsi6_12', 'rush')
                    max = ys[i]
                    if (len(ys) - i - 1) < 2:
                        print(code, self.name, xs[i], 'rsi rush!!!')

            if rsi6[i] < rsi12[i]:
                rush = False
                if run == False and rsi6[i] > 60 and rsi6[i] < 70:
                    run = True
                    self.get_statistics(xs, ys, i, 'rsi6_12', 'run')
                    if (len(ys) - i - 1) < 2:
                        print(code, self.name, xs[i], 'rsi run!!!')

    def get_average(self, price, number):
        average = []
        index = 0
        for i in range(len(price)):
            if i < number:
                index = 0
            else:
                index = i-(number-1)
            p = price[index:i+1]
            average.append(round(np.mean(p), 2))
        return average

    def average_line_select(self, xs, ys):
        ma4 = self.get_average(ys, 4)
        ma9 = self.get_average(ys, 9)
        ma18 = self.get_average(ys, 18)
        # ma60 = self.get_average(ys, 60)

        pre_rush = False
        rush = False
        pre_run = False
        run = False

        ret = False
        code = self.code + ':'
        for i in range(0, len(ys)):
            # rush
            if ma4[i] > ma9[i]:
                if pre_rush == False:
                    pre_rush = True
                    self.get_statistics(xs, ys, i, 'ma4___9', 'rush')
                    # if (len(ys) - i - 1) < 2:
                    #     print(code, self.name, xs[i], 'average pre_rush!')
                if ma9[i] > ma18[i]:
                    if rush == False:
                        rush = True
                        self.get_statistics(xs, ys, i, 'ma9__18', 'rush')
                        plt.scatter(xs[i], ys[i], s=50,
                                    color='red')      # s 为点的 size
                        if (len(ys) - i - 1) < 2:
                            print(code, self.name, xs[i], 'average rush!!!')
                            ret = True

            if ma9[i] < ma18[i]:
                rush = False
            if ma4[i] < ma9[i]:
                if rush == False:
                    pre_rush = False
            # run
            if ma4[i] < ma9[i]:
                if pre_run == False:
                    pre_run = True
                    self.get_statistics(xs, ys, i, 'ma4___9', 'run')
                    # print(code, xs[i], 'pre_run!')
                if ma9[i] < ma18[i]:
                    if run == False:
                        run = True
                        self.get_statistics(xs, ys, i, 'ma9__18', 'run')
                        plt.scatter(xs[i], ys[i], s=50,
                                    color='green')      # s 为点的 size
                        if (len(ys) - i - 1) < 2:
                            print(code, self.name, xs[i], 'average run!!!')

            if ma9[i] > ma18[i]:
                run = False
            if ma4[i] > ma9[i]:
                if run == False:
                    pre_run = False
        plt.plot(xs, ma4, color=self.colors['ma4'],
                 linewidth=1.5, linestyle="-", label='ma4')
        plt.plot(xs, ma9, color=self.colors['ma9'],
                 linewidth=1.5, linestyle="-", label='ma9')
        plt.plot(xs, ma18, color=self.colors['ma18'],
                 linewidth=1.5, linestyle="-", label='ma18')
        # plt.plot(xs, ma60, color=self.colors['ma60'], linewidth=1.5, linestyle="-", label='ma60')
        return ret

    def show(self):
        # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
        plt.figure(figsize=(24, 13.5), dpi=80)
        # 再创建一个规格为 1 x 1 的子图
        plt.subplot(111)
        # fig1, ax = plt.subplots()
        plt.title(self.name)

        xs, ys, amount = self.get_position()

        flag = False
        flag = self.average_line_select(xs, ys)
        # self.rsi_select(xs, ys)
        self.price_select(xs, ys)
        self.amount_price_select(xs, ys, amount)
        high_x, high_y, low_x, low_y = self.get_point(xs, ys)
        self.draw_point(high_x, high_y, low_x, low_y)
        # self.draw_high_line(high_x, high_y)
        # self.draw_low_line(low_x, low_y)

        plt.plot(xs, ys, color='blue', linewidth=1.0,
                 linestyle="-", label="price")
        plt.legend(loc='upper left', ncol=2)   # 图例

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
        xticks = list(range(0, len(xs), 5))
        xlabels = [xs[x] for x in xticks]
        xlabels.append(xs[-1])
        plt.xticks(xlabels, rotation=-90)
        # # 设置纵轴精准刻度
        # plt.yticks([-2, 0, 2, 4, 6, 8, 10],
        #         ["-2m", "0m", "2m", "4m", "6m", "8m", "10m"])
        if flag is True:
            plt.savefig(self.path + self.code + '_' +
                        self.name + '_' + self.freq + '.png')

        filename = './statistics.csv'
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f_csv = csv.writer(f)
                ar2 = [[row[i] for row in statistics]
                       for i in range(len(statistics[0]))]
                f_csv.writerows(ar2)
        else:
            with open(filename, 'a') as f:
                f_csv = csv.writer(f)
                ar2 = [[row[i] for row in statistics]
                       for i in range(len(statistics[0]))]
                f_csv.writerows(ar2)
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

    show = Show(code=csv_file, name=name, freq=freq, path=path)
    show.show()
