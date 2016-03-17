# -*- coding: utf-8 -*-
# 使用环境Python 3.5.1 |Anaconda 2.4.1 (64-bit)
import sys
#print('目前编码为：', sys.getdefaultencoding()) #测试用
import re
import urllib.request# bug ：单引用urllib出错！
import time

#对myurl页面进行seWord匹配查找
#seWord是用unicode表示，可改为utf-8
def getInfo(myurl, seWord):#seword即re.compile的返回值
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    }
    req = urllib.request.Request(
        url=myurl,
        headers=headers
    )
    time.sleep(0.3)
    response = urllib.request.urlopen(req)
    html = response.read().decode()
    timeMatch = seWord.search(html)
    if timeMatch:
        s = timeMatch.groups()
        return s[0]
    else:
        return None
#if  __name__ == '__main__':
#    url1 = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=%s'
#    sexRe = re.compile(u'em>\u6027\u522b</em>(.*?)</li')
#    sex = getInfo(url1%271100, sexRe)
#    print(sex)
#    测试成功

def safeGet(myid, myurl, seWord):
    try:
        return getInfo(myurl, seWord)
    except:
        try:
            return getInfo(myurl, seWord)
        except:
            httperrorfile = open(file5, 'a')
            info = '%d %s\n' % (myid, 'httperror')
            httperrorfile.write(info)
            httperrorfile.close()
            return 'httperror'

def searchWeb(idArr):
    for id in idArr:
        sexUrl = url1 % (id) #将%s替换为id
        timeUrl = url2 % (id)
        sex = safeGet(id,sexUrl, sexRe)
        if not sex: #如果sexUrl里面找不到性别，在timeUrl再尝试找一下
            sex = safeGet(id,timeUrl, sexRe)
        time = safeGet(id,timeUrl, timeRe)
        #上述三行代码如果断网的时候，调用了3次safeGet，每次调用都会往文本里面同一个id写多次httperror

        #如果出现了httperror，需要重新爬取
        if (sex is 'httperror') or (time is 'httperror') :
            pass
        else:
            if sex:
                info = '%d %s' % (id, sex)
                if time:
                    info = '%s %s\n' % (info, time)
                    wfile = open(file1, 'a')
                    wfile.write(info)
                    wfile.close()
                else:
                    info = '%s %s\n' % (info, 'notime')
                    errtimefile = open(file2, 'a')
                    errtimefile.write(info)
                    errtimefile.close()
            else:
                #这儿是性别是None，然后确定一下是不是用户不存在
                #断网的时候加上这个，会导致4个重复httperror
                #可能用户的性别我们无法知道，他没有填写
                notexist = safeGet(id,sexUrl, notexistRe)
                if notexist is 'httperror':
                    pass
                else:
                    if notexist:
                        notexistfile = open(file3, 'a')
                        info = '%d %s\n' % (id, 'notexist')
                        notexistfile.write(info)
                        notexistfile.close()
                    else:
                        unkownsexfile = open(file4, 'a')
                        info = '%d %s\n' % (id, 'unkownsex')
                        unkownsexfile.write(info)
                        unkownsexfile.close()
def main():
    if len(sys.argv) != 3:
        print('usage: python rsspyder.py <startNum> <endNum>')
        sys.exit(-1)
       
    global sexRe,timeRe,notexistRe,url1,url2,file1,file2,file3,file4,startNum,endNum,file5
    startNum = int(sys.argv[1])
    endNum = int(sys.argv[2])

    file1 = 'correct%s-%s.txt' % (startNum, endNum)
    #293001 男 2015-5-1 19:17  正确数据：id、性别、活动时间三者都有
    file2 = 'errTime%s-%s.txt' % (startNum, endNum)
    #2566 女 notime  没有时间：有id、有性别，无活动时间
    file3 = 'notexist%s-%s.txt' % (startNum, endNum)
    #29005 notexist  用户不存在：该id没有对应的用户
    file4 = 'unkownsex%s-%s.txt' % (startNum, endNum)
    #221794 unkownsex  有id，但是性别从网页上无法得知（经检查，这种情况也没有活动时间）
    file5 = 'httperror%s-%s.txt' % (startNum, endNum)
    #271004 httperror  网络错误：网断了，或者服务器故障，需要对这些id重新检查
    
    sexRe = re.compile('em>性别</em>(.*?)</li')#两者都行，应该是都直接转换为unicode编码了
    sexRe = re.compile(u'em>\u6027\u522b</em>(.*?)</li')
    timeRe = re.compile('<li><em>上次发表时间</em>(.*?)</li')
    timeRe = re.compile(u'em>\u4e0a\u6b21\u6d3b\u52a8\u65f6\u95f4</em>(.*?)</li')
    notexistRe = re.compile('(p>)抱歉，您指定的用户空间不存在<')
    notexistRe = re.compile(u'(p>)\u62b1\u6b49\uff0c\u60a8\u6307\u5b9a\u7684\u7528\u6237\u7a7a\u95f4\u4e0d\u5b58\u5728<')
    	
    url1 = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=%s'
    url2 = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=%s&do=profile'
    url3 = "http://rs.xidian.edu.cn/portal.php"

    searchWeb(range(startNum,endNum))
    # numThread = 10
    # searchWeb(xrange(endNum))
    # total = 0
    # for i in xrange(numThread):
    # data = xrange(1+i,endNum,numThread)
    #     total  =+ len(data)
    #     t=threading.Thread(target=searchWeb,args=(data,))
    #     t.start()
    # print total
    
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if  __name__ == '__main__':
    main()