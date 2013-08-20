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


# readdata: pre-process the orderfile
# input: orderfile
# output: trades,portsyms,datelist,date_dict
def readdata(orderfile):
	trades = nu.loadtxt(orderfile,dtype='i4,i4,i4,S5,S5,i4', delimiter=',', comments='#')
	# build equity symbols list
	portsyms = []
	for i in trades:
		portsyms.append(i[3])  # i[3]为symbol所在的位置
	portsyms = {}.fromkeys(portsyms).keys() # list去重操作  
   
   # build dates list
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
	return (trades,portsyms,datelist,date_dict)		


# get_price: generate timestamps and close price for the given time period
# input:  startdate, enddate
# output: timestamps, close	
def time_price(startdate,enddate,portsyms):
	# set the time boundaries
	timestamps = du.getNYSEdays(startdate,enddate,timeofday)
	#get the close price
	dataobj = da.DataAccess(storename)
	close = dataobj.get_data(timestamps, portsyms, closefield)  # close is not the same as 'actual close'
	
	return (timestamps,close)

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

# two kinds of days:
    
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
# price is a dict contains all the symbols price for the trading day
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
	elif ordertype.lower() == 'sell':
		cash += int(share) * float(price[symbol])
		stockhold[symbol] -= share
	else:
		pass
	
	return (cash, stockhold)

# for given stockhold and price, calculate the stockvalue at a special day
# the input: stockhold and price are both directories
# as: {'GOOG':100,'AAPL':100} or {'GOOG':123.45,'AAPL':123}
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

def order_process(totalfund,orderfile):
	
	# process the orderfile
	trades,portsyms,datelist,date_dict = readdata(orderfile)
    
    # get the timestamps, close 
	startdate = datelist[0]
	enddate   = datelist[-1]         #TODO:notice the enddate off-by-1 error
	enddate   = enddate +  dt.timedelta(days=1)
	timestamps,close = time_price(startdate,enddate,portsyms)

	# in the following code, cash, stockhold,stockvalue,totalvalue is updated
	cash = float(totalfund)
	stockvalue = 0.0
	totalvalue = float(totalfund)
	result = []
	# construct the stockhold
	stockhold = {}
	for symbol in portsyms:
		stockhold[symbol] = 0
	
	trade_treated = 0
	
	for time in timestamps:
        # create the price directory 
		price_today = {}
		for sym in portsyms:
			price_today[sym] = close[sym][time]
    	  
		date = time - timeofday    
		
		if date in date_dict:             # at least one order happens that day
			num = date_dict[date]        # get the number of orders of that day
    		while (num > 0):
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
	
	return result

# generate the valuefile based on orders	
def value_generator(totalfund,orderfile,valuefile):
	fundvalue = order_process(totalfund, orderfile)
	nu.savetxt(valuefile,fundvalue,fmt='%f',delimiter=',',newline='\n')
	print 'The value of fund is saved at: %s' % valuefile
          
###############################################
########   main code       ####################
###############################################
#1. read in the argv from command line
totalfund, orderfile, valuefile = argv[1:]

#2. set the datasource 
storename = 'Yahoo'
timeofday=dt.timedelta(hours=16)
closefield = 'close'
if __name__ == '__main__':
	value_generator(totalfund,orderfile,valuefile)
		



		
	
	

























     
   
   
