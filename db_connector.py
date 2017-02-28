# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 09:44:02 2017

@author: Alfred
"""
import csv
import sqlite3
import traceback

import mysql.connector
from sqlalchemy import create_engine
from pymongo import MongoClient


class DBconnector():
    """
    1
    """

    def __init__(self, db_info, database=None):
        """
        1
        """

        self.db_info = db_info

        if database:
            db_info['connection']['database'] = database
        if db_info['type'] == 'mongo':
            self.tbls = self.mongo_cnx()
            
    def sqlite_cnx(self):
        cnx = sqlite3.connect(**self.db_info['connection'])
        return cnx
    
    def mysql_cnx(self, database=None):
        """
        1
        """

        info = self.db_info['connection']
        if database:
            info['database'] = database
        cnx = mysql.connector.connect(**info)
        return cnx

    def mysql_con(self, database=None):
        """
        1
        """

        info = self.db_info['connection']
        if database:
            info['database'] = database
        stmt = 'mysql+mysqlconnector://{user}:{password}@{host}:{port}'\
            '/{database}'
        engine = create_engine(stmt.format(**info))
        return engine.connect()

    def insert(self, tbl, data, **kwargs):
        """
        1
        """
        exsit = [i[0] for i in self.get_pk(tbl)]
        flds, pk = self.db_info['tbls'][tbl]
        flds = kwargs.get('flds', flds)
        num = kwargs.get('num', 20)
        
        values = ','.join([':%s' % i for i in flds])
        stmt = 'insert into {tbl}({flds}) values ({values})'
        stmt = stmt.format(
            tbl = tbl,
            flds = ','.join(flds),
            values = values
        )
        
        update_list=[]
        insert_list=[]
        for i in data:
            if not i:
                continue
            if i[pk] in exsit:
                update_list.append(i)
            else:
                exsit.append(i[pk])
                insert_list.append(i)
            if insert_list and len(insert_list) % num ==0:
                self.execute_many(stmt, insert_list)
                insert_list=[]
            if update_list and len(update_list) % num ==0:
                self.update(tbl, flds, update_list)
                update_list=[]
        if insert_list:
            self.execute_many(stmt, insert_list)
        if update_list:
            self.update(tbl, flds, update_list)
            
    def update(self, tbl, flds, data):
        pk = self.db_info['tbls'][tbl][1]
        stmt = 'update {tbl} set {flds} where {pk}=:{pk}'.format(
            tbl=tbl, flds=','.join(['%s=:%s' %(i,i) for i in flds]), pk=pk
        )
        self.execute_many(stmt, data)

    def insert_from_file(self, file_path, tbl, flds, encoding='utf-8'):
        """
        1
        """

        fobj = open(file_path, encoding=encoding)
        reader = csv.reader(fobj)
        self.insert_from_list(tbl, flds, reader)
        fobj.close()

    def execute(self, stmt):
        """
        1
        """

        cnx = getattr(self, '%s_cnx' % self.db_info['type'])()
        cursor = cnx.cursor()
        cursor.execute(stmt)
        rst = [i for i in cursor]
        cnx.commit()
        cursor.close()
        cnx.close()
        return rst

    def execute_many(self, stmt, data):
        """
        1
        """

        cnx = getattr(self, '%s_cnx' % self.db_info['type'])()
        cursor = cnx.cursor()
        
        for i in self.yield_list(data):
            try:
                cursor.executemany(stmt, data)
                cnx.commit()
            except:
                traceback.print_exc()

        cursor.close()
        cnx.close()

    @staticmethod
    def yield_list(data, num=20):
        pool = []
        for i in data:
            pool.append(i)
            if pool and len(pool) % num == 0:
                yield pool
                pool=[]
        if pool:
            yield pool
            
    def get_pk(self, tbl):
        pk = self.db_info['tbls'][tbl][1]
        return self.execute('select {pk} from {tbl}'.format(pk=pk, tbl=tbl))

    def rename(self, data):
        self.execute_many('update file set path=:dst where path=:src', data)