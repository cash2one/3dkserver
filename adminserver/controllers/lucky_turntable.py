#-*-coding:utf-8-*-
from bottle import route, request, template, redirect, static_file
from util   import current_time
from os.path import isfile, isdir
import os
import sys
from excel import excel_import, excel_export
from utils import pprint

BACK_FILE = 'lucky_turntable_back_up.xls'

field_lucky_turntable = 'TurntableType', 'TotalPay', 'RewardGolds'
del_sql_lucky_turntable = 'DELETE FROM tb_lucky_turntable WHERE TurntableType=%s;'

sql_lucky_turntable   = 'SELECT %s FROM tb_lucky_turntable' % ','.join(field_lucky_turntable)
insert_sql_lucky_turntable   = 'INSERT INTO tb_lucky_turntable (%s) VALUES (%s)' % (','.join(field_lucky_turntable), ','.join(['%s'] * len(field_lucky_turntable)))

field_lucky_turntable_item = 'ID', 'TurntableType', 'ItemType', 'ItemID', 'ItemNum'
sql_lucky_turntable_item   = 'SELECT %s FROM tb_lucky_turntable_item' % ','.join(field_lucky_turntable_item)
insert_sql_lucky_turntable_item = 'INSERT INTO tb_lucky_turntable_item (%s) VALUES (%s)' % (','.join(field_lucky_turntable_item), ','.join(['%s'] * len(field_lucky_turntable_item)))
select_sql_item = 'SELECT %s FROM tb_lucky_turntable_item WHERE TurntableType=%s'

excel_name = 'LuckyTurntable'
excel_export_filename = "LuckyTurntable_%Y%m%d%H%M.xls"

IMPORT_SQLS = {
        excel_name        : [insert_sql_lucky_turntable, 'tb_lucky_turntable'],
        'LuckyTurntableItem' : [insert_sql_lucky_turntable_item, 'tb_lucky_turntable_item'],
    }

EXPORT_SQLS = {
        'tb_lucky_turntable'      : [sql_lucky_turntable,      field_lucky_turntable,      excel_name],
        'tb_lucky_turntable_item' : [sql_lucky_turntable_item, field_lucky_turntable_item, 'LuckyTurntableItem'],
    }

@route("/lucky_turntable")
def lucky_turntable_index(db):
    db.execute(sql_lucky_turntable)
    data = db.fetchall()
    return template('lucky_turntable_index', data=data)

@route("/lucky_turntable/delete", method="POST")
def lucky_turntable_delete(db):
    aid = request.forms.aid.strip()
    #sql = 'DELETE FROM tb_lucky_turntable WHERE ID=%s;' % aid
    sql = del_sql_lucky_turntable % aid

    try:
        db.execute(sql)
        return {'result':0, 'data':''}
    except Exception, e:
        return {'result':1, 'data':str(e)}

@route("/lucky_turntable/import", method="POST")
def lucky_turntable_import(db):
    data = request.files.data
    error = ''
    all_sqls = IMPORT_SQLS 

    if data and data.file:
        tmp_root = './tmp/'
        if not isdir(tmp_root):  # 若目录tmp_root不存在，则创建
            os.mkdir(tmp_root)
        tmp_filename = os.path.join(tmp_root, current_time('tmp_lucky_turntable%Y%m%d%H%M%S.xls'))
        tmp_file = open(tmp_filename, 'w')  # 新建一个xls后缀的文件，然后将读取的excel文件的内容写入该文件中
        rows = data.file.readlines()

        if not rows:  # 文件空
            error = '数据格式错误[2]'
            return template('error', error=error)
        for row in rows:
            tmp_file.write(row)
        tmp_file.close()

        # 在导入新的数据前，先将数据库原有数据导出到tmp目录，作为备份，数据导入失败时可以恢复数据
        export_sqls = EXPORT_SQLS
        try:
            # 若备份文件已存在，则删除重新写入
            if os.path.exists(os.path.join(tmp_root, BACK_FILE)):
                os.remove(os.path.join(tmp_root, BACK_FILE))
            excel_export(export_sqls, tmp_root, BACK_FILE, db)
        except Exception, e:
            print '数据备份错误: %s' %e

        error = excel_import(all_sqls, tmp_filename, db)
        os.remove(tmp_filename)  # 删除上传的临时文件
    else:  # 没有文件
        error = '数据格式错误[1]'

    if error:
        # 导入数据错误，进行数据恢复
        try:
            excel_import(all_sqls, os.path.join(tmp_root, BACK_FILE), db)
            print '数据恢复成功'
        except Exception, e:
            print '数据恢复错误: %s' %e
        return template('error', error=error + '    数据已恢复')
    else:
        redirect("/lucky_turntable")

@route("/lucky_turntable/export")
def lucky_turntable_export(db):
    tmp_root = './tmp/'
    filename = current_time(excel_export_filename)  # 文件名
    error = ''

    if not isfile(tmp_root + filename): 
        all_sqls = EXPORT_SQLS
        error = excel_export(all_sqls, tmp_root, filename, db)

    if error:  
        return template('error', error=error)
    else:
        return static_file(filename, root = tmp_root, download = filename)

@route("/lucky_turntable/recover")
def lucky_turntable_recover(db):
    tmp_root = './tmp/'
    filename = os.path.join(tmp_root, BACK_FILE)
    error = ''
    if not isfile(filename):
        error = '没有备份文件'
        return template('error', error=error)
    all_sqls = IMPORT_SQLS
    error = excel_import(all_sqls, filename, db)
    if error:
        return template('error', error= '数据恢复失败，原因：' + error)
    else:
        redirect('/lucky_turntable')

@route("/lucky_turntable/item/get", method='POST')
def lucky_turntable_item_get(db):
    aid = request.forms.aid.strip()
    db.execute(select_sql_item%( ','.join(field_lucky_turntable_item), aid))
    _data = db.fetchall()
    return {'result': 0 if len(_data) > 0 else 1, 'data': _data}

@route("/lucky_turntable/delitem", method='POST')
def lucky_turntable_item_delete(db):
    turn_id = request.forms.turn_id.strip()
    db.execute('DELETE FROM tb_lucky_turntable_item WHERE ID=%s', (turn_id, ))
    return {'result': 0, 'data': ''}


