# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:59:38 2017

@author: Alfred
"""
import json

from utils.logger import Logger

TOKEN = {
    'ESC':['\''],
    'OPR':[' ', ',', '-'],
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
    
    def __init__(self, item):
        self.item = item

    def create_tbl(self):
        """
        1
        """
        
        stmts = [
            'create table tag (' \
                'id int(11) primary key auto_increment,' \
                'name varchar(32)' \
            ');',
            'create table {item}_tag (' \
                'id int(11) primary key auto_increment, ' \
                '{item}_id int(11),' \
                'tag_id int(11)' \
            ');'.format(item=self.item),
            'create table tag_parent (' \
                'id int(11) primary key auto_increment, ' \
                'tag_id int(11), ' \
                'parent_id int(11) ' \
            ');'
        ]
        return stmts
    
    ########################################################
    def interpret(self,stmt):
        return self.parse_result(*self.parse_parentheses(stmt,[]))

    def parse_result(self, stmt, sub_stmts):
        """
        1
        """
        logger=Logger('Tag')
        
        # Input OPR Check
        for i in enumerate(stmt):
            if i[1] == '[' and i[0] != 0:
                if stmt[i[0] - 1] not in TOKEN['OPR']:
                    logger.error(
                        '<Input> OPR error\nstmt: {stmt}\nPosition: {pos}'\
                        .format(stmt=stmt, pos=i[0])
                    )
                    return ''
            elif i[1] == ']' and i[0] != len(stmt) - 1:
                if stmt[i[0] + 1] not in TOKEN['OPR']:
                    logger.error(
                        '<Input> OPR error\nstmt: {stmt}\nPosition: {pos}'\
                        .format(stmt=stmt, pos=i[0])
                    )
                    return ''

        # Sperate stmt
        fst, opr, last = self.parse_operator(stmt)
        logger.debug('<parse>\nfst: {fst}\nopr: {opr}\nlast: {last}'\
                     .format(fst=fst, opr=opr, last=last))
        # eval fst
        if max([opr in fst for opr in TOKEN['OPR']]) == 1:
            fst = self.parse_result(fst, sub_stmts)
        else:
            fst = self._eval(fst)
            if isinstance(fst, list):
                fst = self.get_tags(sub_stmts[fst[0] - 1], sub_stmts)
            else:
                fst = set([fst])
                logger.debug('<eval> fst: {fst}'.format(fst=fst))
        # eval last
        last = self._eval(last)
        if isinstance(last, list):
            last = self.parse_result(sub_stmts[last[0] - 1], sub_stmts)
        else:
            last = set([last])
            logger.debug('<parse> last: {last}'.format(last=last))

        # calculate
        if opr == '&':
            return self._and(fst, last)
        elif opr == '|':
            return self._or(fst, last)
        elif opr == '-':
            return self._diff(fst, last)
        
    @staticmethod
    def parse_operator(stmt):
        """
        1
        """
        logger=Logger('Tag')
        logger.debug('<Input> stmt: %s' % stmt)
        pos = [
            stmt.replace('\\%s' % opr, '  ').rfind(opr) \
                for opr in TOKEN['OPR']
        ]
        logger.debug('<pos> pos: {pos}'.format(pos=pos))
        pos = max(pos)
        logger.debug('<pos> pos: {pos}'.format(pos=pos))
        return (stmt[: pos], stmt[pos], stmt[pos + 1: ])
    
    def parse_parentheses(self, stmt, sub_stmts):
        """
        1
        """
        logger = Logger('Tag')
        logger.debug('<Input>\nstmt: {stmt}\nsub_stmts: {sub_stmts}'\
                     .format(stmt=stmt, sub_stmts=sub_stmts))
        end = stmt.find(')')
        if end != -1:
            start = stmt.rfind('(', 0, end)
            sub_stmts.append(stmt[start + 1: end])
            stmt = ''.join(
                [stmt[: start], '[%s]' % len(sub_stmts), stmt[end + 1: ]]
            )
            logger.debug('<Output>\nstmt: {stmt}\nsub_stmts: {sub_stmts}'\
                         .format(stmt=stmt, sub_stmts=sub_stmts))
            return self.parse_parentheses(stmt, sub_stmts)
        else:
            return (stmt, sub_stmts)
    
    @staticmethod
    def _and(fst, last):
        """
        1
        """
        logger = Logger('Tag')
        logger.debug('<opr> AND')
        return fst.intersection(last)
    
    @staticmethod
    def _or(fst, last):
        """
        1
        """
        logger = Logger('Tag')
        logger.debug('<opr> OR')
        return fst.union(last)
    
    @staticmethod
    def _diff(fst, last):
        """
        1
        """
        logger = Logger('Tag')
        logger.debug('<opr> DIFF')
        return fst.difference(last)
    
    @staticmethod
    def _eval(data):
        """
        1
        """
        logger=Logger('Tag')
        logger.debug('<Input> data: %s' % data)
        try:
            data = data.replace("'", '"')
            if data.isalpha():
                return data
            else:
                return json.loads(data)
        except:
            logger.error('<data> data: %s' % data)
            raise

    def modify(self, item, tags):
        tags = tags.splite(';')
        self.execute_many('insert ignore into tag (name) values(?)', tags)
        tags = self.execute(
            'select id from tag where name in (%s)' % ','.join(tags)
        )
        tags = [i[0] for i in tags]

        self.execute_many(
            'insert ignore into {item}_tag ({item}_id, tag_id) '\
                'values({item_id},?)'\
                .format(item=self.item, item_id=item),
            tags
        )
        item = self.execute(
            'select id,tag_id from {item}_tag where '\
                'item_id={item_id}'.format(item=self.item, item_id=item)
        )
        delete = []
        for i in item:
            if i[1] not in tags:
                delete.append(i[0])
        self.execute('delete from %s_tag where id in (%s)'\
                     % (self.item, ','.join(delete))
        )
        
    def tag_to_item(self, tag):
        stmt = \
            'SELECT item_id '\
            '  FROM {item}_tag '\
            ' WHERE tag_id={tag} '\
            .format(item=self.item, tag=tag)
        return stmt
    
    def item_to_tag(self, item_id):
        stmt = \
            'SELECT name '\
            '  FROM tag '\
            '  JOIN {item}_tag '\
            '    ON tag.id={item}_tag.tag_id '\
            '  JOIN {item} '\
            '    ON {item}_tag.{item}_id = {item}.isbn '\
            ' WHERE {item}_id={item_id} '\
            .format(item=self.item, item_id=item_id)
        return stmt
    
    @staticmethod
    def parse(text):
        pass