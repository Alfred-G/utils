# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sqlite3

db=r'C:\Program Files (x86)\Thunder Network\Thunder\Profiles\TaskDb.dat'
cnx=sqlite3.connect(db)
cursor=cnx.cursor()

cursor.execute('select * from AccelerateTaskMap303318203_superspeed_1_1 ')
items=cursor.fetchall()
_set=set()
for item in items:
    UserData=item[3]
    for subItem in ['Result":508','Result":509']:
        subItem=subItem.encode()
        if UserData.find(subItem)!=-1:
            LocalTaskId=item[0]
            UserData=UserData.replace(subItem,'Result":0'.encode())
            _set.add(LocalTaskId)
            cursor.execute('update AccelerateTaskMap303318203_superspeed_1_1 '\
                'set UserData=? where LocalTaskId=?',(UserData,LocalTaskId))
            cnx.commit()
            break
cnx.close()
for i in _set:
    print(i)
