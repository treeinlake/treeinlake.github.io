# -*- coding: utf-8 -*-
"""
使用环境 Python 3.5.1 |Anaconda 2.4.1 (64-bit)

使用Popen可以自定义标准输入、标准输出和标准错误输出。我在SAP实习的时候，项目组在linux平台下经常使用Popen，可能是因为可以方便重定向输出。

下面这段代码借鉴了以前项目组的实现方法，Popen可以调用系统cmd命令。下面3个communicate()连在一起表示要等这3个线程都结束。
"""

# coding=utf-8
from subprocess import Popen
import subprocess
import time
#import threading

startn = 1
endn = 300001
step =1000
total = int((endn - startn + 1 ) /step)
ISOTIMEFORMAT='%Y-%m-%d %X'

#hardcode 3 threads
#沒有深究3个线程好还是4或者更多个线程好
#输出格式化的年月日时分秒
#输出程序的耗时（以秒为单位）
for i in range(0,total,3):
    startNumber = startn + step * i
    startTime = time.clock()

    s0 = startNumber
    s1 = startNumber + step
    s2 = startNumber + step*2
    s3 = startNumber + step*3

    p1=Popen(['python', 'rsspyder.py', str(s0),str(s1)],bufsize=10000, stdout=subprocess.PIPE)
#打开文件名不对不会报错？？？
    p2=Popen(['python', 'rsspyder.py', str(s1),str(s2)],bufsize=10000, stdout=subprocess.PIPE)

    p3=Popen(['python', 'rsspyder.py', str(s2),str(s3)],bufsize=10000, stdout=subprocess.PIPE)

    startftime ='[ '+ time.strftime( ISOTIMEFORMAT, time.localtime() ) + ' ] '

    print(startftime + '%s - %s download start... ' %(s0, s1))
    print(startftime + '%s - %s download start... ' %(s1, s2))
    print(startftime + '%s - %s download start... ' %(s2, s3))

    p1.communicate()
    p2.communicate()
    p3.communicate()

    endftime = '[ '+ time.strftime( ISOTIMEFORMAT, time.localtime() ) + ' ] '
    print(endftime + '%s - %s download end !!! ' %(s0, s1))
    print(endftime + '%s - %s download end !!! ' %(s1, s2))
    print(endftime + '%s - %s download end !!! ' %(s2, s3))

    endTime = time.clock()
    print("cost time " + str(endTime - startTime) + " s")
    time.sleep(5)
