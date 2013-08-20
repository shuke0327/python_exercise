# -*- coding: utf-8 -*-
# import Tkinter module
from Tkinter import *

# create a root widget
root = Tk()

# create a label widget, a slave widget 
w= Label(root,text='Hello,world!')

# 只有在pack之后，才能根据Label中的内容，计算好大小，位置，然后显示在屏幕上
w.pack()

# 进入事件循环，接受来自用户的事件，执行对应的事件处理
# 直到用户调用quit()或者窗口被关闭
# mainloop()还要处理内部的widget更新，来自和windows manager的通信
root.mainloop()















