#! /usr/bin/env python
class Time60(object):
'Time60 - track hours and minutes'
	def __init__(self,hr,minu):
		'Time60 constructor - take hours and mins'
		self.hr  = hr
		self.min = minu
	
	def __str__(self):
		'Time60 - string representation'
		return '%d : %d' % (self.hr, self.min)
	__repr__ = __str__
	
	def __add__(self,other):
	'Time60 - overloading the add operator'
		return self.__class__(self.hr+other.hr,\
				self.min+other.min)
	def __iadd__(self,other):
	'Time60 - overloading in-place addition'
		self.hr  += other.hr
		self.min += other.min
		return self 
