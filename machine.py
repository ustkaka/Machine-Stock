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

# 1、提取数据并绘涨跌图 #########################################################
alldays = DayLocator()  
months = MonthLocator() 
month_formatter = DateFormatter("%b %Y")  

#quotes_pre的内容(time, 1_hua, 2_tuo, 3_ji, 4_xin, 5_ai)
quotes_pre = np.loadtxt('E:\AI金融\Machine\machineStocks.csv', delimiter=',', usecols=(0,2,3,4,5,6), converters={0:datestr2num}, unpack=True) 
quotes_s = []
quotes_s.append(quotes_pre[0])
quotes_s.append( 1 + quotes_pre[1]/100 )
quotes_s.append( 1 + quotes_pre[2]/100 )
quotes_s.append( 1 + quotes_pre[3]/100 )
quotes_s.append( 1 + quotes_pre[4]/100 )
quotes_s.append( 1 + quotes_pre[5]/100 )

alldays = DayLocator()  
months = MonthLocator() 
month_formatter = DateFormatter("%b %Y") 

fig = plt.figure(figsize=(100, 9)) 
ax = fig.add_subplot(111) 
ax.xaxis.set_major_locator(months) 
ax.xaxis.set_minor_locator(alldays) 
ax.xaxis.set_major_formatter(month_formatter) 

plt.title("Price Line:5_ai")
plt.xlabel("Day")


plt.plot([quotes_pre[0][0],quotes_pre[0][-1]], [0,0], 'b', lw=0.5 )#画出水平线
## 画出 1_hua 的图形
#plt.plot(quotes_pre[0], quotes_pre[1], c='r', lw=1.0) #画出收盘价折线图
#ax.scatter(quotes_pre[0], quotes_pre[1], s=4, marker='s', c='darkred', alpha=1.0) #画出散点图

## 画出 2_tuo 的图形
#plt.plot(quotes_pre[0], quotes_pre[2],  c='orange', lw=1.0) #画出收盘价折线图
#ax.scatter(quotes_pre[0], quotes_pre[2], s=4, c='darkgoldenrod', alpha=1.0) #画出散点图

## 画出 3_ji 的图形
#plt.plot(quotes_pre[0], quotes_pre[3], c='olive', lw=1.0) #画出收盘价折线图
#ax.scatter(quotes_pre[0], quotes_pre[3], s=4, c='darkolivegreen', alpha=1.0) #画出散点图

## 画出 4_xin 的图形
#plt.plot(quotes_pre[0], quotes_pre[4], c='mediumblue', lw=1.0) #画出收盘价折线图
#ax.scatter(quotes_pre[0], quotes_pre[4], s=4, c='midnightblue', alpha=1.0) #画出散点图

# 画出 5_ai 的图形
plt.plot(quotes_pre[0], quotes_pre[5], c='darkviolet', lw=1.0) #画出收盘价折线图
ax.scatter(quotes_pre[0], quotes_pre[5], s=4, c='indigo', alpha=1.0) #画出散点图

# 画出垂直线
accum_profit_5 = 1
base_profit = 1
for i in range( len(quotes_pre[0])//20 -1 ): #每20个交易日，画出一条垂直线
    plt.plot([quotes_pre[0][20*(i+1)],quotes_pre[0][20*(i+1)]], [-10,10], 'black', lw=0.5 )#画出垂直线
    curr_date = num2date( quotes_pre[0][20*(i+1)] ).strftime("%Y/%m/%d")
    accum_profit_5 = reduce( lambda x,y:x*y, quotes_s[5][ 0 : 20*(i+1) ] ) # 参数为quotes[1]，计算1_hua的累计回报
    plt.text( quotes_pre[0][20*(i+1)], 10, "accum profit:{0}".format( round(accum_profit_5,4) ), alpha=0.5 )
    plt.plot( quotes_pre[0][20*(i+1)], accum_profit_5, 'b-s') #显示累计回报：accum_profit_1
    plt.plot( quotes_pre[0][20*(i+1)], base_profit, 'k-s') # 显示基准值：1
    plt.text( quotes_pre[0][20*(i+1)], -10, curr_date, alpha=0.5 )
    
plt.savefig("E:\AI金融\Machine\Price Line {0}.png".format("5_ai"))
plt.show()





