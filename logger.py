# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:54:43 2017

@author: Alfred
"""
import logging
    
class Logger(logging.Logger):
    
    def __init__(self, name):
        super(Logger, self).__init__(name)
        self.setLevel(logging.DEBUG)
        hdr = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s: %(levelname)s: %(message)s'
        )
        hdr.setFormatter(formatter)
        self.addHandler(hdr)