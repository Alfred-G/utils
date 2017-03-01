# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 14:23:10 2016

@author: Alfred
"""
def get_md5(obj):
    """
    1
    """

    import hashlib
    md5 = hashlib.md5()
    md5.update(obj)
    return md5.hexdigest()

def day(i=0):
    """
    1
    """

    from datetime import datetime as dt
    from datetime import timedelta
    return dt.strftime(dt.today() - timedelta(days=i), '%Y-%m-%d')

def fst_captial(x):
    """
    1
    """

    try:
        idx = int(''.join(str(x.encode('gbk')).split('\\x')[1:]).strip('\''), 16)
    except:
        return x

    if idx < 45218 or idx > 55289:
        return x

    alphabet = {
        '45218':'A', '45253':'B', '45761':'C', '46318':'D', '46826':'E',
        '47010':'F', '47297':'G', '47614':'H', '48119':'J', '49062':'K',
        '49324':'L', '49896':'M', '50371':'N', '50614':'O', '50622':'P',
        '50906':'Q', '51387':'R', '51446':'S', '52218':'T', '52698':'W',
        '52980':'X', '53689':'Y', '54481':'Z',
    }
    keys = list(alphabet.keys())
    keys.sort()
    idx = [idx - int(i) for i in keys]
    for i in idx:
        if i < 0:
            return alphabet[keys[idx.index(i) - 1]]
    return 'Z'

def download(source, target, method):
    """
    1
    """

    from mySpider import mySpider
    s = mySpider()
    open(target, '%sb'%method).write(s.opener.open(source).read())

def partition(data_list, num):
    """
    1
    """

    from math import ceil
    delta = ceil(len(data_list)/num)
    partition = range(0, len(data_list), delta)
    return [data_list[i:i + delta] for i in partition]

def merge(file_path, num=5, cp=''):
    """
    1
    """

    import os
    fobj = open('%s.csv' %file_path, 'w')
    for i in range(num):
        if not os.path.isfile('%s_%s.csv' % (file_path, i)):
            continue
        f = open('%s_%s.csv' % (file_path, i), 'r')
        for l in f:
            fobj.write(l)
        f.close()
    fobj.close()
    if cp:
        import shutil
        shutil.copy('%s.csv', cp)

def yield_list(data, num=20):
    pool = []
    for i in data:
        pool.append(i)
        if pool and len(pool) % num == 0:
            yield pool
            pool=[]
    if pool:
        yield pool