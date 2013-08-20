#!usr/bin/env python
# -*- coding: utf-8 -*-
# title: marketsim.py
# usage:
# python maketsim.py 1000000 orders.csv values.csv
# 0. import 所有的模块

import matplotlib.pyplot as plt           #绘图用
from pylab import *                       #计算用  
from qstkutil import DataAccess as da     #获取数据用  
from qstkutil import qsdateutil as du     #获取数据库中日期的信息
from qstkutil import tsutil as tsu     
import datetime as dt                     #处理日期用 
import numpy    as nu                     #处理csv文件，数据格式等
from sys import argv					  #处理命令行参数用				 


#1. 读取命令行参数
totalfund, orderfile, valuefile = argv[1:]


#2. 读取文档,拆分数据
#input: orderfile,
#output: trades,portsyms,
def readdata()

trades    = nu.loadtxt(orderfile,dtype='i4,i4,i4,S5,S5,i4', delimiter=',', comments='#')
   # trades    = sorted(trades)
   
   # build equity symbols list
portsyms = []
for i in trades:
	portsyms.append(i[3])  # i[3]为symbol所在的位置
portsyms = {}.fromkeys(portsyms).keys() # list去重操作  
   
   # build dates list
   # how to read data into date form?
   
datelist = []
for i in trades:
	date = dt.datetime(i[0],i[1],i[2])
	datelist.append(date)
datelist = sorted(datelist)

# construct a date dict based on datalist
date_dict={}
for elem in datelist:
	if elem in date_dict:
		date_dict[elem] += 1
	else:
		date_dict[elem] = 1
		
#3. 获取相应股票的交易价格
storename = 'Yahoo'
timeofday=dt.timedelta(hours=16)
# set the time boundaries
startdate = datelist[0]
enddate   = datelist[-1]         #TODO:notice the enddate off-by-1 error
enddate   = enddate +  dt.timedelta(days=1)
timestamps = du.getNYSEdays(startdate,enddate,timeofday)

#get the close price
dataobj = da.DataAccess(storename)
close = dataobj.get_data(timestamps, portsyms, 'close')  # close is not the same as 'actual close'
   
# #############################################################
# 如何处理close                                                 # 
# get the pointed close price for the (date, symbol)          #
#
# stockrecord = close.values

#def find_price(symbol,date,close):
#	stockrecord = close[symbol]
#	hoursdelta = dt.timedelta(hours=16)
#	if isinstance(date,'dt.datetime'):
#		date = date + hoursdelta
#	price = stockrecord[date]
#	return price
#################################################################

#4. 现金资产计算
   
 # func: calc the funds for each day


# redesign the kernel:  calculate the stock and the cash value
#2. two kinds of days:
    
'''
   2.1 the day in trade_datelist
   update cash  : from price and the share ,calc the cash change
   update stock holds: stockhods[symbol] changes + or -
   update stockvalue:  from symbol,we know the share and the price, and calc the total value
   get the totalfund value for that day
   store the result in a dataFrame, indexed by the day
   
   2.2 the day is not in trade_datelist
   get the price for each symbols
   cash doesnot change cash = cash
   stockholds doesnot change, stockholds = stockholds
   update stockvalue: from stockholds get shares , and times the price for each symbol
   get the total fund value for that day
   store the result in a pandas dataFrame, indexed by the day
''' 
# process the single order , return cash and stockhold 
def cal_trades(cash, order, price,stockhold):
	symbol_loc = 3
	ordertype_loc = 4
	share_loc = 5
	symbol = order[symbol_loc]
	ordertype = order[ordertype_loc]
	share = order[share_loc]
	if ordertype.lower() == 'buy':
		cash -= int(share) * float(price[symbol])  #update cash amount
		stockhold[symbol] += share          #update stockhold
	else:
		cash += int(share) * float(price[symbol])
		stockhold[symbol] -= share
	return (cash, stockhold)

# for given stockhold and price, calculate the stockvalue at a special day
def cal_stockvalue(stockhold, price):
	stockvalue = 0.0                #should be float
	for equity in stockhold:
		stockvalue += stockhold[equity] * price[equity]
	return stockvalue

# scan the timestamps, calculate for each value(cash, stockhold, stockvalue, totalvalue)

#initial the data structure.
#   param cash: record the cash flow
#   param stockholds: a directory, record the symbol:shares pair.
#   param stock value: calculate the stock value recorded in stockhold   
cash = float(totalfund)
stockvalue = 0.0

# build stockhold
stockhold = {}
for symbol in portsyms:
	stockhold[symbol] = 0

totalvalue = float(totalfund)

# initialize some params
trade_treated = 0   # used as flag for different values in one day
result = []
hoursdelta = dt.timedelta(hours=16)

# in the following code, cash, stockhold,stockvalue,totalvalue is updated
for time in timestamps:
    # create the price directory 
    price_today = {}
    for sym in portsyms:
        price_today[sym] = close[sym][time]
    
    # process the very day  
    date = time - hoursdelta    
    if date in datelist:             # at least one order happens that day
    	num = date_dict[date]        # get the number of orders of that day
    	while (num>0):
    		order = trades[trade_treated]
    		cash, stockhold = cal_trades(cash, order, price_today,stockhold)
    		trade_treated += 1               # add trade_cnt by 1, to get the date of next order
    		num -= 1
	else:  # if there is no trading that day
		pass
       
    stockvalue = cal_stockvalue(stockhold, price_today)
    totalvalue = cash + stockvalue    		
   
    # construct a list for result
    record_date = [date.year, date.month, date.day]
    valuerecord = record_date
    valuerecord.append(totalvalue)
    result.append(valuerecord)
    
# write to files
nu.savetxt(valuefile,result,fmt='%d,%d,%d,%.3f',delimiter=',',newline='\n')
print 'heres'
print 'OK,now'       		     
          

###############################################
########   main code       ####################
###############################################







		
	
	

























     
   
   
