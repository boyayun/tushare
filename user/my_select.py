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
import heapq

l = {}

def get_stocks():
    stocks = []
    for key, value in l.items():
        if len(value) < 3:
            # print(key, len(value))
            continue
        total_score = []
        all_code = []
        all_name = []

        all_total = []
        all_pe = []
        all_pb = []
        all_roe = []
        all_grossprofit_margin = []
        all_ratio_cfps_eps = []
        all_or_yoy = []
        all_netprofit_yoy = []
        for v in value:
            all_total.append(v['total'])
            all_pe.append(v['pe'])
            all_code.append(v['code'])
            all_name.append(v['name'])
            all_pb.append(v['pb'])
            all_roe.append(v['roe'])
            all_grossprofit_margin.append(v['grossprofit_margin'])
            all_ratio_cfps_eps.append(v['ratio_cfps_eps'])
            all_or_yoy.append(v['or_yoy'])
            all_netprofit_yoy.append(v['netprofit_yoy'])

        # print(all_name)
        average_pe = np.mean(all_pe)
        if average_pe >= -1 and average_pe <= 1:
            average_pe = 1
        average_pb = np.mean(all_pb)
        if average_pb >= -1 and average_pb <= 1:
            average_pb = 1
        average_roe = np.mean(all_roe)
        if average_roe >= -1 and average_roe <= 1:
            average_roe = 1
        average_grossprofit_margin = np.mean(all_grossprofit_margin)
        if average_grossprofit_margin >= -1 and average_grossprofit_margin <= 1:
            average_grossprofit_margin = 1
        average_ratio_cfps_eps = np.mean(all_ratio_cfps_eps)
        if average_ratio_cfps_eps >= -1 and average_ratio_cfps_eps <= 1:
            average_ratio_cfps_eps = 1
        average_or_yoy = np.mean(all_or_yoy)
        if average_or_yoy >= -1 and average_or_yoy <= 1:
            average_or_yoy = 1
        average_netprofit_yoy = np.mean(all_netprofit_yoy)
        if average_netprofit_yoy >= -1 and average_netprofit_yoy <= 1:
            average_netprofit_yoy = 1

        # print(average_pe, average_pb, average_roe, average_grossprofit_margin, average_ratio_cfps_eps, average_or_yoy)

        for v in value:
            score = (average_pb - v['pb'])/abs(average_pb)
            score += (v['roe'] - average_roe)/abs(average_roe)
            score += (v['grossprofit_margin'] - average_grossprofit_margin)/abs(average_grossprofit_margin)
            score += (v['ratio_cfps_eps'] - average_ratio_cfps_eps)/abs(average_ratio_cfps_eps)
            score += (v['or_yoy'] - average_or_yoy)/abs(average_or_yoy)*0.5
            # score += (v['netprofit_yoy'] - average_netprofit_yoy)/abs(average_netprofit_yoy)*0.5
            total_score.append(round(score,2))

        number = int(len(total_score)/10)+1
        re1 = map(total_score.index, heapq.nlargest(number, total_score)) #求最大的三个索引    nsmallest与nlargest相反，求最小
        # print(key, total_score)
        # print(key, all_pb)
        # print(key, all_roe)
        # print(key, all_grossprofit_margin)
        # print(key, all_ratio_cfps_eps)
        # print(key, all_or_yoy)
        temp = list(re1)
        # print(temp)
        for i in temp:
            # print(i)
            # print(all_code[i], all_name[i], all_pe[i], all_pb[i], all_roe[i], all_grossprofit_margin[i], all_ratio_cfps_eps[i], all_or_yoy[i])
            if all_total[i] > 1000000:
                stocks.append([all_code[i], all_name[i], key, len(value), round(all_total[i], 2), round(all_pe[i], 2), round(all_pb[i], 2), round(all_roe[i], 2),
                round(all_grossprofit_margin[i], 2), round(all_ratio_cfps_eps[i], 2), round(all_or_yoy[i], 2), round(all_netprofit_yoy[i], 2)])

    return stocks

class Select(object):
    def __init__(self, data=None, code='', path='./stocks/', industry='Unknown', name = '', freq = 'D'):
        signal.signal(signal.SIGINT, self.signal_handler)
        if path == '':
            self.path = './'
        else:
            self.path = path + '/'

        self.name = name
        self.code = code
        self.industry = industry
        self.file = code + '_finance.csv'
        self.freq = freq

        # 日线价格
        csv_data = pd.read_csv(self.path + self.code + '_price_' + freq + '.csv', usecols = [3])  # 读取数据
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
        if self.freq == 'D':
            if len(self.price) < 60:
                # print('次新股:', self.code, self.name)
                return False
        elif self.freq == 'W':
            if len(self.price) < 12:
                # print('次新股:', self.code, self.name)
                return False

        date = str(self.end_date[0])
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
            # print('error:', self.code, self.name, f)
            return False

        if self.eps[0] <= 0 or self.bps[0] == 0:
            # print('error:', self.code, self.name)
            return False
        pe = self.price[0]/self.eps[0]*f
        pb = self.price[0]/self.bps[0]
        roe = self.roe[0]/f

        #  单位(万)
        total = self.price[0]*(self.extra_item[0]+self.profit_dedt[0])/self.eps[0]/10000
        # if total < 1000000:
            # print('市值小于100亿:', self.code, self.name, total)
            # return False

        ratio_cfps_eps = self.ocfps[0] / self.eps[0]

        # if self.grossprofit_margin[0] < 0 or self.ocfps[0] or self.or_yoy[0] < 0 or self.netprofit_yoy[0] < 0:
        #     return False
        if self.industry not in l.keys():
            l[self.industry] = []
        all_data = {}
        all_data['code'] = self.code
        all_data['name'] = self.name
        all_data['pe'] = pe
        all_data['pb'] = pb
        all_data['roe'] = roe
        all_data['grossprofit_margin'] = self.grossprofit_margin[0]
        all_data['ratio_cfps_eps'] = ratio_cfps_eps
        all_data['or_yoy'] = self.or_yoy[0]
        all_data['netprofit_yoy'] = self.netprofit_yoy[0]
        all_data['total'] = total

        l[self.industry].append(all_data)

        # print(l)

        # if total > 1000000 and pb < 10 and roe > 20 and self.grossprofit_margin[0] > 30 and ratio_cfps_eps > 0.75 and self.or_yoy[0] > 10:
        # print(self.code, self.name, end=': ')
        # print('total:', total,end='; ')
        # print('pe:', pe, end='; ')
        # print('pb:', pb,end='; ')
        # print('roe:', roe,end='; ')
        # print('grossprofit_margin:', round(self.grossprofit_margin[0], 2), end='; ')
        # print('ratio_cfps_eps:', ratio_cfps_eps)
        return True

if __name__ == "__main__":
    code = sys.argv[1]
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

    select = Select(code = code, name = name, path=path, freq=freq)
    select.select()
    print(get_stocks())