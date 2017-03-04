# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 15:00:40 2017

@author: Alfred
"""
import os
from time import strftime, localtime

from utils.functions import get_md5

class FileOpr():

    @staticmethod
    def scan(path):
        """
        1
        """

        for p, ds, fs in os.walk(path):
            for f in os.scandir(p):
                if f.is_file():
                    file = {}
                    file['path'] = f.path
                    file['ctime'] = strftime('%Y-%m-%d',
                        localtime(f.stat().st_ctime))
                    size = f.stat().st_size
                    file['size'] = round(size / 1024 / 1024, 2)
                    #fobj = open(f.path, 'rb')
                    file['md5'] = ''#get_md5(fobj.read())
                    #fobj.close()
                    yield file

    @staticmethod
    def open_file(file_path):
        if os.path.isfile(file_path):
            os.system(file_path)

    @staticmethod
    def rename(data):
        """
        1
        """

        for i in data:
            os.rename(**data)

    @staticmethod
    def remove(data):
        for i in data:
            os.remove(i)
