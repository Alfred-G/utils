# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 15:00:40 2017

@author: Alfred
"""
import os
from time import strftime, localtime
import traceback
import logging

from utils.logger import Logger

class FileOpr():
    """
    1
    """
    @staticmethod
    def scan(path):
        logger = Logger('FileOpr')
        logger.setLevel(logging.INFO)
        logger.info('<start> scan start')
        for p, ds, fs in os.walk(path):
            logger.info('<path> %s' % p)
            for f in os.scandir(p):
                if f.is_file():
                    file = {}
                    file['path'] = f.path.replace('\\','/')
                    file['ctime'] = strftime('%Y-%m-%d',
                        localtime(f.stat().st_ctime))
                    size = f.stat().st_size
                    file['size'] = round(size / 1024 / 1024, 2)

                    yield file
                    logger.debug('<scaned> %s' % f.path)
        logger.info('<end> scan complete')

    @staticmethod
    def rename(src, dst):
        logger = Logger('FileOpr')
        if not os.path.isfile(src):
            logger.error('<src> source file not exsits\nsrc: %s' % src)
            return False
        if not os.path.isdir(os.path.dirname(dst)):
            logger.error('<dst> dst dir not exsits\ndst: %s' % dst)
            return False
        if os.path.isfile(dst):
            logger.error('<dst> dst conflict\ndst: %s' % dst)
            return False
        try:
            os.rename(src, dst)
            return True
        except:
            logger.error(
                '<unkown> {err}\nsrc: {src}\ndst:{dst}'\
                .format(err=traceback.print_exc(), src=src, dst=dst)
            )
            return False

    @staticmethod
    def open_file(path):
        logger = Logger('FileOpr')
        if os.path.exists(path):
            try:
                os.startfile(path)
                return True
            except:
                logger.error(
                    '<unkown> {err}\npath:{path}'\
                    .format(err=traceback.print_exc(), path=path)
                )
                return False
        else:
            logger.error('<path> path not exsits\npath: %s' % path)
            return False