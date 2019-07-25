# coding=utf-8
'''
Created on 2016-10-26
@author: Jennifer
Project:读取mysql数据库的数据，转为json格式
'''
import json
import pymysql
import os
import sys


def TableToJson(key):
    conn = pymysql.Connect(host='localhost', user='root',
                           passwd='123456', db='weibo', port=3306, charset='utf8')
    cur = conn.cursor()
    # try:
    # 1-7：如何使用python DB API访问数据库流程的
    # 1.创建mysql数据库连接对象connection
    # connection对象支持的方法有cursor(),commit(),rollback(),close()
    # 3.编写sql
    sql = "SELECT f.mid, f.pid, f.rootknot, u.userName " \
          "FROM {}_findsons f, {}_userinfo u WHERE f.userid = u.userid".format(
              key, key)
    # 4.执行sql命令
    # execute可执行数据库查询select和命令insert，delete，update三种命令(这三种命令需要commit()或rollback())
    cur.execute(sql)
    # 5.获取数据
    # fetchall遍历execute执行的结果集。取execute执行后放在缓冲区的数据，遍历结果，返回数据。
    # 返回的数据类型是元组类型，每个条数据元素为元组类型:(('第一条数据的字段1的值','第一条数据的字段2的值',...,'第一条数据的字段N的值'),(第二条数据),...,(第N条数据))
    data = cur.fetchall()
    # 6.关闭cursor

    json_file = {}
    jsonData = []
    jsonLink = []
    jsonCatamid = []
    jsonCata_temp_mid = []
    jsonCata_new_mid = []
    # 循环读取元组数据
    # 将元组数据转换为列表类型，每个条数据元素为字典类型:[{'字段1':'字段1的值','字段2':'字段2的值',...,'字段N:字段N的值'},{第二条数据},...,{第N条数据}]
    for row in data:
        temp_result = {}
        if row[1] == '-1':
            continue
        else:
            temp_result['name'] = row[2]
            jsonCatamid.append(temp_result)

    for id in jsonCatamid:
        if id not in jsonCata_temp_mid:
            jsonCata_temp_mid.append(id)
    print(jsonCata_temp_mid)

    for id in jsonCata_temp_mid:
        result = "帖子{}".format(jsonCata_temp_mid.index(id)+1)
        jsonCata_new_mid.append({'name': result})
    print(jsonCata_new_mid)
    json_file['categories'] = jsonCata_new_mid
    for row in data:
        result = {}
        if row[1] == '-1':
            continue
        else:
            result['name'] = row[0]
            result['username'] = row[3]
            dict = {}
            dict['name'] = row[2]
            result['category'] = jsonCata_new_mid[jsonCata_temp_mid.index(
                dict)]['name']
            if row[1] == '0':
                result['symbolSize'] = [20, 20]
            else:
                pass
            jsonData.append(result)
    json_file['type'] = "force"
    json_file['nodes'] = jsonData

    for row in data:
        result = {}
        if row[1] == '-1':
            continue
        else:
            if row[1] == '0':
                result['source'] = row[0]
            else:
                result['source'] = row[1][1:]
            result['target'] = row[0]
            jsonLink.append(result)
    json_file['links'] = jsonLink
    cur.close()

    conn.close()
    return json_file

    # except:
    #     print('MySQL connect fail...')


if __name__ == '__main__':
    kw = sys.argv[1]
    print(kw)
    # 以读写方式w+打开文件，路径前加r，防止字符转义
    jsonData = TableToJson(kw)

    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    print(jsondatar)
    f = open(r'getdata.json', 'w+', encoding="utf8")
    # 写数据
    f.write(jsondatar)
    # 关闭文件
    f.close()


def writefile(kw):
    jsonData = TableToJson(kw)
    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    print(jsondatar)
    f = open(r'static/getdata.json', 'w+', encoding="utf8")
    # 写数据
    f.write(jsondatar)
    # 关闭文件
    f.close()
