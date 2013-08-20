#!usr/bin/env python
# -*- coding: utf-8 -*-

#usage:
# python analysis.py values.csv $SPY
#import modules

import matplotlib.pyplot as plt           #绘图用
from pylab import *                       #计算用  
from qstkutil import DataAccess as da     #获取数据用  
from qstkutil import qsdateutil as du     #获取数据库中日期的信息
from qstkutil import tsutil as tsu     
import datetime as dt                     #处理日期用 
import numpy    as nu                     #处理csv文件，数据格式等
from sys import argv					  #处理命令行参数用				 

#1. read in the argv
valuefile = argv[1]
bench_symbol = argv[2]
if not isinstance(bench_symbol,str):
	bench_symbol = str(bench_symbol)

#2. read in the data
datelist = []
fundvalue = []
funddata = nu.loadtxt(valuefile, delimiter=',', dtype='i4,i4,i4,f8') #  values = readcsv(valuefile)
for record in funddata:
	fundvalue.append(record[3])
	date = dt.datetime(record[0],record[1],record[2])
	datelist.append(date)

   
#3. read in the $SPY data
timeofday = dt.timedelta(hours=16)
startdate = datelist[0]
enddate   = datelist[-1] + dt.timedelta(days=1)  # fix the off-by-1 error
timestamps = du.getNYSEdays(startdate,enddate, timeofday)

# get the value for benchmark
dataobj = da.DataAccess('Yahoo')
symbols = [bench_symbol]
close = dataobj.get_data(timestamps,symbols,'close')
benchmark_price = []
benchmark_value = []
for time in timestamps:
	benchmark_price.append(close[bench_symbol][time])
    
bench_shares = fundvalue[0]/benchmark_price[0]
for i in range(len(fundvalue)):
	benchmark_value.append(bench_shares*benchmark_price[i])
	


# benchmark_value is a array contents only price value
   
#4. plot the history price for fund and benchmark
plt.clf()
fig = plt.figure()
fig.add_subplot(111)
plt.plot(timestamps,fundvalue,alpha=0.4)
plt.plot(timestamps,benchmark_value)
names = ['fund',bench_symbol]
plt.legend(names)
plt.ylabel('History Price')
plt.xlabel('Date')
fig.autofmt_xdate(rotation=45)
savefig('/home/shuke0327/python/report.pdf',format='pdf')

# 5. calculate the measurement for fund and benckmark
# TODO: compare to the algorithm provided by the qstk, choose the better one
# calculate the daily return of fund and benchmark
def daily_return(value):
	daily_ret = []
	daily_ret.append(0)   #the daily_return of the first trading day
	for i in range(1,len(value)):
		daily_ret.append((value[i]/value[i-1])-1)
	return daily_ret

# calculate the average 
def cal_average(value):
	daily_ret = daily_return(value)
	average = mean(daily_ret)
	return average
	
# calculate the stdv 
def cal_std(value):
	daily_ret = daily_return(value)
	std_value = std(daily_ret)
	return std_value
	
# calculate the sharpe-ratio
def cal_sharpe(value,days):
	average = cal_average(value)
	std_value = cal_std(value)
	sharpe_ratio = (sqrt(days)*average)/std_value
	return sharpe_ratio
	
# output the ratio
print '####################################################'
print
print 'total return for fund is: %f ' % (fundvalue[-1]/fundvalue[0] - 1)
print 'average for fund is: %f ' % cal_average(fundvalue)
print 'std value for fund is: %f' % cal_std(fundvalue)
print 'sharperatio of fund is %f' % cal_sharpe(fundvalue,len(timestamps))
print
print '####################################################'
print
print 'total return for benchmark is: %f' % (benchmark_value[-1]/benchmark_value[0]-1)
print 'average daily return for benchmark is: %f' % cal_average(benchmark_value)
print 'std value for benchmark is: %f' % cal_std(benchmark_value)
print 'sharpe_ratio of benchmark is: %f' % cal_sharpe(benchmark_value, len(timestamps))
print
print '####################################################'
