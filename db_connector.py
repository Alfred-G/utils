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


class DBconnector():
    """
    1
    """

    def __init__(self, db_info, database=None):
        """
        1
        """

        if database:
            db_info['connection']['database'] = database
        self.db_info = db_info

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

        cnx = getattr(self, '%s_cnx' % self.db_info['type'])()
        cursor = cnx.cursor()
        cursor.execute(stmt)
        cnx.commit()
        for i in cursor:
            yield i
        cursor.close()
        cnx.close()

    def execute_many(self, stmt, data, num=20):
        """
        1
        """

        cnx = getattr(self, '%s_cnx' % self.db_info['type'])()
        cursor = cnx.cursor()

        for i in yield_list(data, num):
            try:
                cursor.executemany(stmt, i)
                cnx.commit()
            except:
                traceback.print_exc()

        cursor.close()
        cnx.close()

    def sqlite_insert(self, tbl, data, **kwargs):
        """
        1
        """

        flds, pk = self.db_info['tbls'][tbl]
        flds = kwargs.get('flds', flds)
        num = kwargs.get('num', 20)

        stmt = 'insert or ignore into {tbl} values (:{pk})'\
            .format(tbl=tbl, pk=pk),

        self.execute_many(stmt, data, num)
        self.update(tbl, flds, data, num)

    def update(self, tbl, flds, data, num=20):
        """
        1
        """

        pk = self.db_info['tbls'][tbl][1]
        stmt = 'update {tbl} set {flds} where {pk}=:{pk}'.format(
            tbl=tbl,
            flds=','.join(['%s=:%s' % (i, i) for i in flds]),
            pk=pk
        )
        self.execute_many(stmt, data, num)

    def get_pk(self, tbl):
        """
        1
        """

        pk = self.db_info['tbls'][tbl][1]
        return self.execute(
            'select {pk} from {tbl}'.format(pk=pk, tbl=tbl)
        )
