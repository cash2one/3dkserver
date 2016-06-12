#-*-coding:utf-8-*-
from bottle import route, request, template, redirect, static_file
from util   import current_time
from os.path import isfile, isdir
import os
import sys
from excel import excel_import, excel_export
from utils import pprint

BACK_FILE = 'limit_fellow_back_up.xls'

field_limit_fellow = 'ActivityID', 'ActivityName', 'IsOpen', 'MonsterList'
del_sql_limit_fellow = 'DELETE FROM tb_limit_fellow WHERE ActivityID=%s;'

sql_limit_fellow   = 'SELECT %s FROM tb_limit_fellow' % ','.join(field_limit_fellow)
insert_sql_limit_fellow   = 'INSERT INTO tb_limit_fellow (%s) VALUES (%s)' % (','.join(field_limit_fellow), ','.join(['%s'] * len(field_limit_fellow)))

field_limit_fellow_desc = 'ActivityID', 'DescTurn', 'FellowDesc'
sql_limit_fellow_desc   = 'SELECT %s FROM tb_limit_fellow_desc' % ','.join(field_limit_fellow_desc)
insert_sql_limit_fellow_desc = 'INSERT INTO tb_limit_fellow_desc (%s) VALUES (%s)' % (','.join(field_limit_fellow_desc), ','.join(['%s'] * len(field_limit_fellow_desc)))
select_sql_desc = 'SELECT %s FROM tb_limit_fellow_desc WHERE ActivityID=%s'

excel_name = 'LimitFellow'
excel_export_filename = "LimitFellow_%Y%m%d%H%M.xls"

IMPORT_SQLS = {
        excel_name        : [insert_sql_limit_fellow, 'tb_limit_fellow'],
        'LimitFellowDesc' : [insert_sql_limit_fellow_desc, 'tb_limit_fellow_desc'],
    }

EXPORT_SQLS = {
        'tb_limit_fellow'      : [sql_limit_fellow,      field_limit_fellow,      excel_name],
        'tb_limit_fellow_desc' : [sql_limit_fellow_desc, field_limit_fellow_desc, 'LimitFellowDesc'],
    }

@route("/limit_fellow")
def limit_fellow_index(db):
    db.execute(sql_limit_fellow)
    data = db.fetchall()
    return template('limit_fellow_index', data=data)

@route("/limit_fellow/delete", method="POST")
def limit_fellow_delete(db):
    aid = request.forms.aid.strip()
    #sql = 'DELETE FROM tb_limit_fellow WHERE ID=%s;' % aid
    sql = del_sql_limit_fellow % aid

    try:
        db.execute(sql)
        return {'result':0, 'data':''}
    except Exception, e:
        return {'result':1, 'data':str(e)}

@route("/limit_fellow/import", method="POST")
def limit_fellow_import(db):
    data = request.files.data
    error = ''
    all_sqls = IMPORT_SQLS 

    if data and data.file:
        tmp_root = './tmp/'
        if not isdir(tmp_root):  # 若目录tmp_root不存在，则创建
            os.mkdir(tmp_root)
        tmp_filename = os.path.join(tmp_root, current_time('tmp_limit_fellow%Y%m%d%H%M%S.xls'))
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
        redirect("/limit_fellow")

@route("/limit_fellow/export")
def limit_fellow_export(db):
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

@route("/limit_fellow/recover")
def limit_fellow_recover(db):
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
        redirect('/limit_fellow')

@route("/limit_fellow/desc/get", method='POST')
def limit_fellow_desc_get(db):
    aid = request.forms.aid.strip()
    db.execute(select_sql_desc%( ','.join(field_limit_fellow_desc), aid))
    _data = db.fetchall()
    return {'result': 0 if len(_data) > 0 else 1, 'data': _data}

@route("/limit_fellow/deldesc", method='POST')
def limit_fellow_desc_delete(db):
    turn_id = request.forms.turn_id.strip()
    db.execute('DELETE FROM tb_limit_fellow_desc WHERE DescTurn=%s', (turn_id, ))
    return {'result': 0, 'data': ''}


