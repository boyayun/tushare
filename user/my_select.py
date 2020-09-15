#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import signal
import time
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np                # 导入模块 numpy，并简写成 np

class Select(object):
    def __init__(self, data=None, code='', path='./stocks/', name = ''):
        signal.signal(signal.SIGINT, self.signal_handler)
        if path == '':
            self.path = './'
        else:
            self.path = path + '/'

        self.name = name
        self.code = code
        self.file = code + '_finance.csv'

        # 日线价格
        csv_data = pd.read_csv(self.path + self.code, usecols = [6])  # 读取数据
        self.price = [i[0] for i in csv_data.values.tolist()]
        # print(self.price)

        # 期末日期
        csv_data = pd.read_csv(self.path + self.file, usecols = ['end_date'])
        self.end_date = [i[0] for i in csv_data.values.tolist()]

        # 每股净利润
        csv_data = pd.read_csv(self.path + self.file, usecols = ['eps'])
        self.eps = [i[0] for i in csv_data.values.tolist()]

        # 每股净资产
        csv_data = pd.read_csv(self.path + self.file, usecols = ['bps'])
        self.bps = [i[0] for i in csv_data.values.tolist()]

        # 净资产收益率
        csv_data = pd.read_csv(self.path + self.file, usecols = ['roe'])
        self.roe = [i[0] for i in csv_data.values.tolist()]

        # 非经常性损益
        csv_data = pd.read_csv(self.path + self.file, usecols = ['extra_item'])
        self.extra_item = [i[0] for i in csv_data.values.tolist()]

        # 扣除非经常性损益后的净利润
        csv_data = pd.read_csv(self.path + self.file, usecols = ['profit_dedt'])
        self.profit_dedt = [i[0] for i in csv_data.values.tolist()]

        # 销售毛利率
        csv_data = pd.read_csv(self.path + self.file, usecols = ['grossprofit_margin'])
        self.grossprofit_margin = [i[0] for i in csv_data.values.tolist()]

        # 归属母公司股东的净利润同比增长率(%)
        csv_data = pd.read_csv(self.path + self.file, usecols = ['netprofit_yoy'])
        self.netprofit_yoy = [i[0] for i in csv_data.values.tolist()]

        # 每股经营活动产生的现金流量净额
        csv_data = pd.read_csv(self.path + self.file, usecols = ['ocfps'])
        self.ocfps = [i[0] for i in csv_data.values.tolist()]

        # 营业收入同比增长率
        csv_data = pd.read_csv(self.path + self.file, usecols = ['or_yoy'])
        self.or_yoy = [i[0] for i in csv_data.values.tolist()]

    def signal_handler(self, signal, frame):
        sys.exit(0)

    def select(self):
        date = str(self.end_date[0])
        if len(self.price) < 60:
            print('次新股:', self.code, self.name)
            return False

        f = 1
        if date.find('1231') >= 0:
            f = 1
        elif date.find('0930') >= 0:
            f = 0.75
        elif date.find('0630') >= 0:
            f = 0.5
        elif date.find('0331') >= 0:
            f = 0.25
        else:
            print('error:', self.code, self.name, f)
            return False

        if self.eps[0] == 0 or self.bps[0] == 0:
            print('error:', self.code, self.name)
            return False
        pe = round(self.price[0]/self.eps[0]*f, 2)
        pb = round(self.price[0]/self.bps[0], 2)
        roe = round(self.roe[0]/f, 2)

        #  单位(万)
        total = round(self.price[0]*(self.extra_item[0]+self.profit_dedt[0])/self.eps[0]/10000,2)

        ratio_cfps_eps = round(self.ocfps[0] / self.eps[0], 2)

        if total > 1000000 and pb < 10 and roe > 20 and self.grossprofit_margin[0] > 30 and ratio_cfps_eps > 0.75 and self.or_yoy[0] > 10:
            print(self.code, self.name, end=': ')
            print('total:', total,end='; ')
            print('pe:', pe, end='; ')
            print('pb:', pb,end='; ')
            print('roe:', roe,end='; ')
            print('grossprofit_margin:', round(self.grossprofit_margin[0], 2), end='; ')
            print('ratio_cfps_eps:', ratio_cfps_eps)
            return True

        return False

if __name__ == "__main__":
    csv_file = sys.argv[1]
    name = ''
    path = './stocks/'

    if len(sys.argv) == 4:
        path = sys.argv[3]
        name = sys.argv[2]
    elif len(sys.argv) == 3:
        name = sys.argv[2]

    select = Select(code = csv_file, name = name, path=path)
    print(select.select())