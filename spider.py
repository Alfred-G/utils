# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 09:34:10 2017

@author: Alfred
"""
import os
import time
import types
import socket
import urllib.request
import urllib.parse
import http.cookiejar
import traceback

from lxml import etree


HEADER = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;'\
        ' rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Accept-Language': 'zh-CN',
    'Accept-Encoding': 'gzip, deflate',
}


def xpath(self, state):
    """
    1
    """

    return self.etree.xpath(state)


def make_a_try(func):
    def _make_a_try(self, url, **kwargs):
        try:
            return func(self, url, **kwargs)
        except:
            traceback.print_exc()
            return
    return _make_a_try
    
    
class Spider():
    """
    1
    """

    def __init__(self, **kwargs):
        header = kwargs.get('header', HEADER)
        handler = self.get_handler(**kwargs.get('handler', {}))
        self.opener = self.get_opener(header, handler)
        socket.setdefaulttimeout(kwargs.get('timeout', 3))

    @staticmethod
    def get_opener(header, handler):
        """
        1
        """

        opener = urllib.request.build_opener(*handler)
        opener.addheaders = header
        urllib.request.install_opener(opener)
        return opener

    def get_handler(self, **kwargs):
        """
        1
        """

        handler = []
        if kwargs.get('cookie', False):
            handler.append(self.cookie_handler())
        if kwargs.get('proxy', ''):
            handler.append(self.proxy_handler(kwargs.get('proxy', '')))
        return handler

    @staticmethod
    def cookie_handler():
        """
        1
        """

        cookie_jar = http.cookiejar.CookieJar()
        return urllib.request.HTTPCookieProcessor(cookie_jar)

    @staticmethod
    def proxy_handler(proxy):
        """
        1
        """

        proxydict = {
            'http': 'http://%s' % proxy,
        }
        return urllib.request.ProxyHandler(proxydict)

    @make_a_try
    def request(self, url, **kwargs):
        """
        1
        """

        post_dict = urllib.parse.urlencode(kwargs.get('post_dict', {}))\
            .encode(kwargs.get('encoding', 'utf-8'))
        try:
            if post_dict:
                response = self.opener.open(url, post_dict)
            else:
                response = self.opener.open(url)
        except:
            traceback.print_exc()
            return

        response.body = response.read()
        response.etree = etree.HTML(response.body)
        response.xpath = types.MethodType(xpath, response)

        time.sleep(kwargs.get('sleep', 0))
        return response

    def get_imgs(self, img_path, img_urls, **kwargs):
        prefix = kwargs.get('prefix','')
        suffix = kwargs.get('suffix','')
        sleep = kwargs.get('sleep','')
        
        for img_url in img_urls:
            img_url = img_url + suffix
            file_name = os.path.join(img_path, prefix + os.path.basename(img_url))
            if not os.path.isfile(file_name):
                try:
                    img = self.opener.open(img_url)
                    data = img.read()
                    fobj = open(file_name,'wb')
                    fobj.write(data)
                    fobj.close()
                    if sleep:
                        time.sleep(sleep)
                except socket.timeout:
                    print (img_url+' time out')
                except:
                    print (img_url+' download fail')
                    print(traceback.print_exc())

    @staticmethod
    def extract(data, idx=0):
        if data and len(data) > idx:
            return data[idx]
        return ''