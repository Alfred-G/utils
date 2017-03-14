# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 09:44:02 2017

@author: Alfred
"""
import sqlite3
import traceback

import mysql.connector
from sqlalchemy import create_engine

from utils.functions import yield_list
from utils.logger import Logger

class DBcon():
    """
    1
    """

    def __init__(self, db_info, database=None):
        """
        1
        """

        if database and db_info['type'] != 'mongo':
            db_info['connection']['database'] = database
        self.db_info = db_info

    """
    cnx
    """
    def sqlite_cnx(self):
        """
        1
        """

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

    def execute(self, stmt):
        """
        1
        """

        logger = Logger('DBcon')
        cnx = getattr(self, '%s_cnx' % self.db_info['type'])()
        cursor = cnx.cursor()
        try:
            cursor.execute(stmt)
            for i in cursor:
                yield i
            cnx.commit()
        except:
            logger.error(
                '<unknown> {err}\nstmt: {stmt}'\
                .format(err=traceback.print_exc(), stmt=stmt)
            )
        finally:
            cursor.close()
            cnx.close()

    def execute_many(self, stmt, data, num=20):
        """
        1
        """
        logger = Logger('DBcon')
        if not isinstance(data, list):
            logger.error('<data> data is not list\n%s' % data)

        try:
            cnx = getattr(self, '%s_cnx' % self.db_info['type'])()
            cursor = cnx.cursor()

            cursor.executemany(stmt, data)
            cnx.commit()
        except:
            logger.error(
                '<unknown> {err}\nstmt: {stmt}\ndata: {data}'\
                .format(err=traceback.print_exc(), stmt=stmt, data=data[0])
            )
        finally:
            cursor.close()
            cnx.close()

    def sqlite_insert(self, tbl, data, **kwargs):
        """
        1
        """
        
        try:
            logger = Logger('DBcon')
            
            flds, pk = self.db_info['tbls'][tbl]
            logger.debug('<pk> %s' % pk)
            logger.debug('<flds> first: %s' % flds)
            flds = [i[0] for i in flds]
            logger.debug('<flds> second: %s' % flds)
            flds = kwargs.get('flds', flds)
            logger.debug('<flds> final: %s' % flds)
            num = kwargs.get('num', 20)
            
            stmt = 'insert or ignore into {tbl}({pk}) values (:{pk})'\
                .format(tbl=tbl, pk=pk)
            logger.debug('<stmt> %s' % stmt)
            for i in yield_list(data, num):
                if not kwargs.get('test', False):
                    self.execute_many(stmt, i, num)
                    logger.info('<write> INSERT operated')
                    self.update(tbl, flds, i, num)
                else:
                    print(stmt)
                    print(i[0])
                    break
        except:
            logger.error(
                '<unknown> {err}\nstmt: {stmt}\ndata: {data}'\
                .format(err=traceback.print_exc(), stmt=stmt, data=data[0])
            )

    def update(self, tbl, flds, data, **kwargs):
        """
        1
        """
        try:
            logger = Logger('DBcon')
            
            pk = self.db_info['tbls'][tbl][1]
            logger.debug('<pk> %s' % pk)
            num = kwargs.get('num', 20)
            if kwargs.get('pk', False):
                stmt = 'update {tbl} set {flds} where {pk}=:_pk'.format(
                    tbl = tbl,
                    flds=','.join(['%s=:%s' % (i, i) for i in flds]),
                    pk=pk
                )
                logger.info('<pk> update PK')
                logger.debug('<stmt> %s' % stmt)
            else:
                stmt = 'update {tbl} set {flds} where {pk}=:{pk}'.format(
                    tbl = tbl,
                    flds=','.join(['%s=:%s' % (i, i) for i in flds]),
                    pk=pk
                )
                logger.debug('<stmt> %s' % stmt)
                
            for i in yield_list(data, num):
                if not kwargs.get('test', False):
                    self.execute_many(stmt, i, num)
                    logger.info('<write> UPDATE operated')
                else:
                    print(stmt)
                    print(i[0])
                    break
        except:
            logger.error(
                '<unknown> {err}\nstmt: {stmt}\ndata: {data}'\
                .format(err=traceback.print_exc(), stmt=stmt, data=data[0])
            )

    @staticmethod
    def mongo_cnx(user, password, host, port, database):
        from pymongo import MongoClient
        client = MongoClient(host, int(port))
        database = client.car
        database.authenticate(user, password)
        return database
