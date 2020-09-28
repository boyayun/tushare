#!/usr/bin/python3
# -*- coding:utf-8 -*-
import tushare as ts
import os
import sys
import pandas as pd
import time
from datetime import timedelta
from datetime import datetime
import tushare.stock as stock
from show import Show
from my_select import Select
import my_select
import pandas
import signal
import csv


def fetch_kline_data(code, freq, start):
    filename = './stocks/' + code + '_price_' + freq + '.csv'
    # if not os.path.exists(filename):
    end_date = datetime.strftime(datetime.now(), '%Y%m%d')  # 获取当前时间
    outputflag = True
    api = ts.pro_api()
    while outputflag:  # 循环判断，直到返还的数据为空
        data = ts.pro_bar(api=api, ts_code=code, start_date=start,
                          end_date=end_date, asset='E', freq=freq, adj='qfq')
        # print('data:', data)

        if isinstance(data, pandas.core.frame.DataFrame):
            if data.empty is True:
                outputflag = False
            else:
                # 计算下次请求数据的截止日期
                temp = datetime.strptime(data.iloc[-1]['trade_date'],
                                         '%Y%m%d')
                # print(temp)
                # print(timedelta(hours=24))
                next_end_date = temp - timedelta(hours=24)
                end_date = datetime.strftime(next_end_date, '%Y%m%d')
                # 写csv文件
                if os.path.exists(filename):
                    data.to_csv(filename, header=None, mode='a')  # 追加写入模式
                else:
                    data.to_csv(filename, header=None, mode='a')
        else:
            outputflag = False


def fetch_finance_indicator(code):
    filename = './stocks/' + code + '_finance.csv'
    if not os.path.exists(filename):
        end_date = datetime.strftime(datetime.now(), '%Y%m%d')
        outputflag = True
        api = ts.pro_api()
        while outputflag:
            data = api.fina_indicator(ts_code=code, end_date=end_date)
            if data.empty == True:
                outputflag = False
            else:
                next_end_date = datetime.strptime(
                    data.iloc[-1]['end_date'], '%Y%m%d') - timedelta(hours=24)
                end_date = datetime.strftime(next_end_date, '%Y%m%d')
                if os.path.exists(filename):
                    data.to_csv(filename, header=None, mode='a')
                else:
                    data.to_csv(filename)


if __name__ == '__main__':
    # 设置Token
    ts.set_token('4e5a2ec168a5d1108211422dd7a1b1ca8b3ecd35c799ec6f170e92a1')
    # 初始化接口
    ts_api = ts.pro_api()

    update = 0    # 0:不更新, 1:更新精选股的技术数据， 2:更新已选股的技术数据，3:更新所有股的财务数据
    freq = 'D'
    start = ''
    if len(sys.argv) == 4:
        update = sys.argv[3]
        freq = sys.argv[2]
        start = sys.argv[1]
    elif len(sys.argv) == 3:
        freq = sys.argv[2]
        start = sys.argv[1]
    elif len(sys.argv) == 2:
        start = sys.argv[1]

    if update == 3:
        os.remove('./stocks/*')
    elif update == 2:
        files = './stocks/*_price_' + freq + '*'
        os.remove(files)
    elif update == 1:
        if os.path.exists('./stocks.csv'):
            csv_data = pd.read_csv('./stocks.csv', header=None)  # 读取数据
            data = csv_data.values.tolist()
            for i in data:
                # print(i)
                code = i[0]
                name = i[1]

                price_name = './stocks/' + code + '_price_' + freq + '.csv'
                if os.path.exists(price_name):
                    os.remove(price_name)

    # 股票列表
    stocks = ts_api.stock_basic(
        exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # for i in range(0, len(stocks['ts_code'])):            # len(stocks['ts_code'])
    #     code = stocks['ts_code'][i]
    #     name = stocks['name'][i]
    #     industry = stocks['industry'][i]
    #     if industry == '汽车整车':
    #         print(code, name, industry)
    # exit(0)

    with open('stocks.csv', 'w') as f:
        f_csv = csv.writer(f)
        # len(stocks['ts_code'])
        for i in range(0, len(stocks['ts_code'])):
            code = stocks['ts_code'][i]
            name = stocks['name'][i]
            industry = stocks['industry'][i]
            if (code.find('60') == 0 or code.find('002') == 0 or code.find('000') == 0) and name.find('ST') < 0:   # 主板股票去除ST
                # print(code, name)

                # 更新财务数据
                finance_name = './stocks/' + code + '_finance.csv'
                if not os.path.exists(finance_name):
                    # print(code, name)
                    fetch_finance_indicator(code)
                    time.sleep(1.2)

                # 更新股价
                price_name = './stocks/' + code + '_price_' + freq + '.csv'
                if not os.path.exists(price_name):
                    fetch_kline_data(code, freq, start)
                    if freq == 'D':
                        if os.path.exists(price_name):
                            df = pd.read_csv(price_name, header=None)  # 读取数据
                            cols = list(df)
                            cols.insert(3, cols.pop(cols.index(6)))
                            cols.pop(cols.index(0))
                            df = df.loc[:, cols]
                            df.to_csv(price_name, header=None)
                        time.sleep(0.1)
                    else:
                        time.sleep(0.4)

                # 选股
                if os.path.exists(finance_name) and os.path.exists(price_name):
                    select = Select(
                        code=code, name=name, industry=industry, path='./stocks/', freq=freq)
                    select.select()
        stocks = my_select.get_stocks()
        # print(stocks)
        f_csv.writerows(stocks)
        f.flush()

    # 技术面选股+可视化
    if os.path.exists('./stocks.csv'):
        csv_data = pd.read_csv('./stocks.csv', header=None)  # 读取数据
        data = csv_data.values.tolist()
        for i in data:
            # print(i)
            code = i[0]
            name = i[1]
            if os.path.exists(price_name):
                cmd = './user/show.py ' + code + ' ' + name + ' ' + freq
                # print(cmd)
                os.system(cmd)

    # # 业务预告
    # forecast = ts_api.forecast(ann_date='20190131',
    #                        fields='ts_code,ann_date,end_date,type,p_change_min,p_change_max,net_profit_min')
    # print(forecast)

    # # 分红送股数据
    # dividend = ts_api.dividend(ts_code='600848.SH', fields='ts_code,div_proc,stk_div,record_date,ex_date')
    # print(dividend)

    # # 业绩快报
    # express = ts_api.express(ts_code='600000.SH', start_date='20180101', end_date='20180701',
    #                       fields='ts_code,ann_date,end_date,revenue,operate_profit,total_profit,n_income,total_assets')
    # print(express)

    # # 财务指标数据
    # fina_indicator =  ts_api.fina_indicator(ts_code='600000.SH')
    # print(fina_indicator)

    # # 财务审计意见
    # fina_audit =  ts_api.fina_audit(ts_code='600000.SH', start_date='20100101', end_date='20180808')
    # print(fina_audit)

    # # 主营业务构成
    # fina_mainbz =  ts_api.fina_mainbz(ts_code='000627.SZ', type='P')
    # print(fina_mainbz)

    # # 上市公司完整财务指标获取
    # fetch_finance_indicator('603986.SH')

    # 指数基本信息
    # MSCI:MSCI指数
    # CSI:中证指数
    # SSE:上交所指数
    # SZSE:深交所指数
    # CICC:中金所指数
    # SW:申万指数
    # index_basic = ts_api.index_basic(market='CSI')
    # print(index_basic)

    # # 指数日线行情
    # index_daily = ts_api.index_daily(ts_code='399300.SZ', start_date='20190101', end_date='20190910')
    # print(index_daily)

    # # 指数周线行情
    # index_weekly = ts_api.index_weekly(ts_code='399300.SZ', start_date='20190101', end_date='20190910')
    # print(index_weekly)

    # # 指数月线行情
    # index_monthly = ts_api.index_monthly(ts_code='399300.SZ', start_date='20190101', end_date='20190910')
    # print(index_monthly)

    # # 指数成分和权重
    # index_weight = ts_api.index_weight(index_code='399300.SZ', start_date='20180901', end_date='20190930')
    # print(index_weight)

    # 港股通10大成交股
    # ggt_top10 = ts_api.ggt_top10(trade_date='20190925')
    # print(ggt_top10)

    # # 融资融券交易汇总
    # margin = ts_api.margin(trade_date='20190925')
    # print(margin)

    # # 融资融券交易明细
    # margin_detail = ts_api.margin_detail(trade_date='20190925')
    # print(margin_detail)

    # # 前十大股东
    # top10_holders = ts_api.top10_holders(ts_code='600000.SH', start_date='20190101', end_date='20191231')
    # print(top10_holders)

    # # 前十大流通股东
    # top10_floatholders = ts_api.top10_floatholders(ts_code='600000.SH', start_date='20190101', end_date='20191231')
    # print(top10_floatholders)

    # # 龙虎榜每日明细
    # top_list = ts_api.top_list(trade_date='20190925')
    # print(top_list)

    # # 龙虎榜机构交易明细
    # top_inst = ts_api.top_inst(trade_date='20190925')
    # print(top_inst)

    # # 大宗交易
    # block_trade = ts_api.block_trade(start_date='20190101', end_date='20191231')
    # print(block_trade)

    # # 股票开户数据
    # stk_account = ts_api.stk_account(start_date='20190101', end_date='20191231')
    # print(stk_account)

    # # 股东人数
    # stk_holdernumber = ts_api.stk_holdernumber(ts_code='603986.SH')
    # print(stk_holdernumber)

    # # fund_basic = ts_api.fund_basic(market='E')
    # # print(fund_basic)

    # # data = ts.get_rrr()
    # # print(data)

    # # 新闻联播文字播报
    # cctv_news = ts_api.cctv_news(date='20200902')
    # cctv_news.to_csv('cctv_news.txt')

    # # lpr利率
    # shibor_lpr = ts_api.shibor_lpr(start_date='20190101', end_date='20200903')
    # print('lpr利率:', shibor_lpr)

    # # us_tycr = ts_api.us_tycr(start_q='2018Q1', end_q='2019Q3', fields='quarter,gdp,gdp_yoy')
    # us_tycr = ts_api.us_tycr(start_q='2018Q1', end_q='2019Q3')
    # print('us_tycr:', us_tycr)

    # # GDP
    # cn_gdp = ts_api.cn_gdp(start_q='2018Q1', end_q='2020Q4')
    # print('cn_gdp:', cn_gdp)

    # get_latest_news = ts.get_notices() #显示最新5条新闻，并打印出新闻内容
    # print(get_latest_news)
