# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 21:52:34 2016

@author: Alfred
"""
import os
import time
import traceback
import socket
import urllib.request
import urllib.parse
import http.cookiejar
from lxml import etree

class mySpider:

    def __init__(self,head=None,proxy=None,code='utf-8',timeout=3):
        self.code = code
        self.opener = self.getOpener(self.getHandler(proxy),self.getHeader(head))
        if timeout!= 0:
            socket.setdefaulttimeout(timeout)
 
    def getOpener(self,handler,header):
        opener = urllib.request.build_opener(*handler)
        opener.addheaders = header
        urllib.request.install_opener(opener)
        return opener
    
    def getHandler(self,proxy):
        handler=[]
        cj = http.cookiejar.CookieJar()
        handler.append(urllib.request.HTTPCookieProcessor(cj))
        if proxy:
            proxydict = dict()
            proxydict['http'] = "http://%s" %':'.join(proxy.split(','))
            handler.append(urllib.request.ProxyHandler(proxydict))
        return handler
        
    def getHeader(self,head):
        header = []
        if head==None:
            head = {
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;'\
                ' rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
                }
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        return header
        
    def getPage(self,url,postDict={},sleep=0.05,code=None,err=None):
        response = ''
        postDict = urllib.parse.urlencode(postDict).encode(self.code)
        try:
            if postDict:
                response = Response(url,self.opener.open(url,postDict).read())
            else:
                response = Response(url,self.opener.open(url).read())
        except:
            traceback.print_exc()   
        time.sleep(sleep)
        return response

    def saveImg(self,imgPath=None,imgs=[],prefix='',suffix='',sleep=None):
        for img in imgs:
            imgUrl = img+suffix
            fileName = os.path.join(imgPath,prefix+os.path.basename(imgUrl))
            if not os.path.exists(fileName):
                try:
                    img = self.opener.open(imgUrl)
                    data = img.read()
                    f = open(fileName,'wb')
                    f.write(data)
                    f.close()
                    if sleep:
                        time.sleep(sleep)
                except socket.timeout:
                    print (imgUrl+' time out')
                except:
                    print (imgUrl+' download fail')
                    print(traceback.print_exc())
    
class Response():
    def __init__(self,url,body):
        self.url=url
        self.body=body
        self.etree=etree.HTML(body)
        
    def xpath(self,state):
        return self.etree.xpath(state) 