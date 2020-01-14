# -*- coding: utf-8 -*-
"""
Created on Wed Apr  17 21:40:13 2019

@author: Administrator
"""
import numpy as np
import matplotlib.pyplot as plt
#import sys 
from matplotlib.dates import DateFormatter 
from matplotlib.dates import DayLocator 
from matplotlib.dates import MonthLocator 
from matplotlib.dates import date2num, num2date
from datetime import datetime
from functools import reduce

#import tushare as ts

def datestr2num(s): 
    date1 = datetime.strptime(s.decode('ascii'), "%Y/%m/%d").date()
    date = date2num(date1)
    return date

###############################################################################
############################ 一、标准化数据 ################################

# 1、提取数据 #########################################################
alldays = DayLocator()  
months = MonthLocator() 
month_formatter = DateFormatter("%b %Y")  

#quotes_pre的内容(time, 1_hua, 2_tuo, 3_ji, 4_xin, 5_ai)
quotes_pre = np.loadtxt('E:\AI金融\Machine\machineStocks.csv', delimiter=',', usecols=(0,2,3,4,5,6), converters={0:datestr2num}, unpack=True) 
quotes_s = [] # 存储净值
quotes_s.append(quotes_pre[0])
quotes_s.append( 1 + quotes_pre[1]/100 )
quotes_s.append( 1 + quotes_pre[2]/100 )
quotes_s.append( 1 + quotes_pre[3]/100 )
quotes_s.append( 1 + quotes_pre[4]/100 )
quotes_s.append( 1 + quotes_pre[5]/100 )

quotes_t = [] # 存储新策略下的涨幅 0:时间 1:涨跌幅 2：股票序号

alldays = DayLocator()  
months = MonthLocator() 
month_formatter = DateFormatter("%b %Y") 

fig = plt.figure(figsize=(100, 9)) 
ax = fig.add_subplot(111) 
ax.xaxis.set_major_locator(months) 
ax.xaxis.set_minor_locator(alldays) 
ax.xaxis.set_major_formatter(month_formatter) 

plt.title("Price Line:together1")
plt.xlabel("Day")

# 2、应用策略，获得新策略下净值 #########################################################
quotes_t.append( quotes_pre[0] ) # quotes_t[0]:时间
quotes_t.append( np.zeros( len(quotes_pre[0]) ) ) # quotes_t[1]:涨幅, 默认为0
quotes_t.append( np.ones( len(quotes_pre[0]) ) ) # quotes_t[2]:股票序号, 默认为1
quotes_t[1][0] = quotes_pre[1][0] #修改初始股票价格

curr_stock = 1 #股票序号, 默认为1
for i in range( 0,len(quotes_pre[0])-1 ):
    #先找到5只股票中涨幅最低但不等于0.0001（即停牌）的股票
    a1, a2, a3, a4, a5 = quotes_pre[1][i], quotes_pre[2][i], quotes_pre[3][i], quotes_pre[4][i], quotes_pre[5][i]
    if quotes_pre[1][i] in (0.0001, 0.0002, -0.0001): a1 = 20 # 该股票停牌 或 停牌后涨停、跌停，去除他被选中的可能性
    if quotes_pre[2][i] in (0.0001, 0.0002, -0.0001): a2 = 20 # 该股票停牌 或 停牌后涨停、跌停，去除他被选中的可能性
    if quotes_pre[3][i] in (0.0001, 0.0002, -0.0001): a3 = 20 # 该股票停牌 或 停牌后涨停、跌停，去除他被选中的可能性
    if quotes_pre[4][i] in (0.0001, 0.0002, -0.0001): a4 = 20 # 该股票停牌 或 停牌后涨停、跌停，去除他被选中的可能性
    if quotes_pre[5][i] in (0.0001, 0.0002, -0.0001): a5 = 20 # 该股票停牌 或 停牌后涨停、跌停，去除他被选中的可能性
    
    stock_min_index = 1 + np.argmin( np.array([a1, a2, a3, a4, a5]) )
    if quotes_pre[curr_stock][i] - quotes_pre[stock_min_index][i] >= 4: #差值超过4个百分点，换成跌幅最大股票
        quotes_t[1][i+1] = quotes_pre[stock_min_index][i+1] # 换上新股票，计入新股票涨幅
        curr_stock = stock_min_index # 更换股票序号
        quotes_t[2][i+1] = curr_stock
    else:
        quotes_t[1][i+1] = quotes_pre[curr_stock][i+1] # 仍持有原股票，计入原股票涨幅
        quotes_t[2][i+1] = curr_stock

quotes_t_s = [] # 存储净值
quotes_t_s.append( quotes_t[0] )
quotes_t_s.append( 1 + quotes_t[1]/100 )
quotes_t_s.append( quotes_t[2] )

# 3、画出涨跌图 #####################################################################
## 画出 together1 的图形
#plt.plot(quotes_t[0], quotes_t[1], 'crimson', lw=1.0) #画出收盘价折线图
#ax.scatter(quotes_t[0], quotes_t[1], s=4, marker='s', c='darkred', alpha=1.0) #画出散点图
#plt.plot([quotes_t[0][0],quotes_t[0][-1]], [0,0], 'b', lw=0.5 )#画出水平线

plt.text( quotes_t[0][0], quotes_t[1][0], quotes_t[2][0], alpha=0.5 )#标记初始股票序号

# 画出 together1 的图形
for i in range( len(quotes_t[0]) - 1 ):
    if quotes_t[2][i] == 1:
        plt.plot(quotes_t[0][i:i+2], quotes_t[1][i:i+2], c='r', lw=1.0) #画出收盘价折线图
    elif quotes_t[2][i] == 2:
        plt.plot(quotes_t[0][i:i+2], quotes_t[1][i:i+2], c='orange', lw=1.0) #画出收盘价折线图
    elif quotes_t[2][i] == 3:
        plt.plot(quotes_t[0][i:i+2], quotes_t[1][i:i+2], c='olive', lw=1.0) #画出收盘价折线图
    elif quotes_t[2][i] == 4:
        plt.plot(quotes_t[0][i:i+2], quotes_t[1][i:i+2], c='mediumblue', lw=1.0) #画出收盘价折线图
    elif quotes_t[2][i] == 5:
        plt.plot(quotes_t[0][i:i+2], quotes_t[1][i:i+2], c='darkviolet', lw=1.0) #画出收盘价折线图
    if i>0 and quotes_t[2][i] != quotes_t[2][i-1]:
        curr_date = num2date( quotes_t[0][i] ).strftime("%m/%d")
        plt.text( quotes_t[0][i], quotes_t[1][i], "d:{0},s:{1}".format(curr_date, quotes_t[2][i]), alpha=0.5 )#标记新换股票序号

ax.scatter(quotes_t[0], quotes_t[1], s=4, marker='s', c='darkred', alpha=1.0) #画出散点图
plt.plot([quotes_t[0][0],quotes_t[0][-1]], [0,0], 'b', lw=0.5 )#画出水平线

# 画出垂直线
accum_profit_1 = 1
base_profit_1 = 1
for i in range( len(quotes_t[0])//20 -1 ): #每20个交易日，画出一条垂直线
    plt.plot([quotes_t[0][20*(i+1)],quotes_t[0][20*(i+1)]], [-10,10], 'black', lw=0.5 )#画出垂直线
    curr_date = num2date( quotes_t[0][20*(i+1)] ).strftime("%Y/%m/%d")
    accum_profit_1 = reduce( lambda x,y:x*y, quotes_t_s[1][ 0 : 20*(i+1) ] ) # 参数为quotes[1]，计算1_hua的累计回报
    plt.text( quotes_t[0][20*(i+1)], 10, "accum profit:{0}".format( round(accum_profit_1,4) ), alpha=0.5 )
    plt.plot( quotes_t[0][20*(i+1)], accum_profit_1, 'b-s') #显示累计回报：accum_profit_1
    plt.plot( quotes_t[0][20*(i+1)], base_profit_1, 'k-s') # 显示基准值：1
    plt.text( quotes_t[0][20*(i+1)], -10, curr_date, alpha=0.5 )
    
plt.savefig("E:\AI金融\Machine\Price Line {0}.png".format("together"))
plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
