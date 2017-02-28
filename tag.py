# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:59:38 2017

@author: Alfred
"""
import json


TOKEN = {
    'ESC':['\''],
    'OPR':['&', '|', '-'],
    'PAR':[('(', ')')],
}

TBL = {
    'tag': (['id', 'name'], 'id'),
    'tag_item': (['id', 'tag_id', 'item_id'], 'id'),
    'tag_relation': (['id', 'tag_id', 'parent_id'], 'id'),
}
class Tag():
    """
    1
    """    

    @staticmethod
    def create_tbl(item):
        """
        1
        """
        
        stmts = [
            'create table tag (' \
                'id int(11) primary key,' \
                'name varchar(32)' \
            ');',
            'create table {item}_tag (' \
                'id int(11) primary key, ' \
                '{item}_id int(11),' \
                'tag_id int(11)' \
            ');'.format(item=item),
            'create table tag_parent (' \
                'id int(11) primary key, ' \
                'tag_id int(11), ' \
                'parent_id int(11) ' \
            ');'
        ]
        return stmts
    
    def interpret(self, stmt, sub_stmts):
        """
        1
        """
    
        fst, opr, last = self.operator(stmt)
        if max([opr in fst for opr in TOKEN['OPR']]) == 1:
            fst = self.get_tags(fst, sub_stmts)
        else:
            fst = self._eval(fst)
            if isinstance(fst, list):
                fst = self.get_tags(sub_stmts[fst[0] - 1], sub_stmts)
            else:
                fst = set([fst])
    
        last = self._eval(last)
        if isinstance(last, list):
            last = self.get_tags(sub_stmts[last[0] - 1], sub_stmts)
        else:
            last = set([last])
    
        if opr == '&':
            return self._and(fst, last)
        elif opr == '|':
            return self._or(fst, last)
        elif opr == '-':
            return self._diff(fst, last)
        
    @staticmethod
    def operator(stmt):
        """
        1
        """
    
        pos = [
            stmt.replace('\\%s' % opr, '  ').rfind(opr) for opr in TOKEN['OPR']
        ]
        pos = max(pos)
        return (stmt[: pos], stmt[pos], stmt[pos + 1: ])
    
    def parentheses(self, stmt, sub_stmts=[]):
        """
        1
        """
    
        end = stmt.find(')')
        if end != -1:
            start = stmt.rfind('(', 0, end)
            sub_stmts.append(stmt[start + 1: end])
            stmt = ''.join(
                stmt[: start], '[%s]' % len(sub_stmts), stmt[end + 1: ]
            )
            return self.parentheses(stmt, sub_stmts)
        else:
            return (stmt, sub_stmts)
    
    @staticmethod
    def _and(fst, last):
        """
        1
        """
    
        return fst.intersection(last)
    
    @staticmethod
    def _or(fst, last):
        """
        1
        """
    
        return fst.union(last)
    
    @staticmethod
    def _diff(fst, last):
        """
        1
        """
    
        return fst.difference(last)
    
    @staticmethod
    def _eval(data):
        """
        1
        """
    
        data = data.replace("'", '"')
        if data.isalpha():
            return data
        else:
            return json.loads(data)
