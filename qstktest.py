#!usr/bin/env python
# -*- coding: utf-8 -*-
#  learn to treat the csv format files
# for tutorial 2
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import datetime as dt

# for tutorial 3
# data sources: QSTK/Examples/tutorial3portfolio.csv


# define the data source
filepath = '/home/shuke0327/QSTK/Examples/Basic/example-data.csv'

# read in the data, divide it up
data     = np.loadtxt(filepath, delimiter=',', skiprows=1) #type: 'numpy.ndarray'
								#method: numpy.ndarray.shape will give a tuple of dimensions as result	
pricedat = data[:, 3:]              #split the data of stock price, the format: data[row,col]
									# the pricedat and datesdat type is also: numpy.ndarray
datesdat = np.int_(data[:, 0:3])    #split usage: data[:,0:3] for all rows and the col 0,1,2 .col3 is 										# not included. don't make mistake here.
pricesnames = ['SPY','XOM','GOOG','GLD'] # list type

print "first five rows of price data:"
print pricedat[:5, :]
print
print "first five rows of dates data:"
print datesdat[:5, :]

#First, we create date objects from the date data: 
dates = []
for i in range(0,datesdat.shape[0]):                     # all the rows
	dates.append(dt.date(datesdat[i,0],datesdat[i,1],datesdat[i,2]))

#ready to display the data
plt.clf()                 #clear all the previous plot on the graph
for i in range(0,pricedat.shape[1]):
	plt.plot(dates, pricedat[:,i])
plt.legend(pricesnames)
plt.xlabel('Adjusted Close')
plt.ylabel('Date')
savefig('/home/shuke0327/adjustedclose.pdf',format='pdf')  # is a method from the moudle: pylab

	
'''
 method of numpy.ndarray
 ['T', '__abs__', '__add__', '__and__', '__array__', '__array_finalize__', '__array_interface__', '__array_prepare__', '__array_priority__', '__array_struct__', '__array_wrap__', '__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__delslice__', '__div__', '__divmod__', '__doc__', '__eq__', '__float__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__', '__idiv__', '__ifloordiv__', '__ilshift__', '__imod__', '__imul__', '__index__', '__init__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__', '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__', '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__nonzero__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__setitem__', '__setslice__', '__setstate__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__xor__', 'all', 'any', 'argmax', 'argmin', 'argsort', 'astype', 'base', 'byteswap', 'choose', 'clip', 'compress', 'conj', 'conjugate', 'copy', 'ctypes', 'cumprod', 'cumsum', 'data', 'diagonal', 'dot', 'dtype', 'dump', 'dumps', 'fill', 'flags', 'flat', 'flatten', 'getfield', 'imag', 'item', 'itemset', 'itemsize', 'max', 'mean', 'min', 'nbytes', 'ndim', 'newbyteorder', 'nonzero', 'prod', 'ptp', 'put', 'ravel', 'real', 'repeat', 'reshape', 'resize', 'round', 'searchsorted', 'setasflat', 'setfield', 'setflags', 'shape', 'size', 'sort', 'squeeze', 'std', 'strides', 'sum', 'swapaxes', 'take', 'tofile', 'tolist', 'tostring', 'trace', 'transpose', 'var', 'view']
'''

