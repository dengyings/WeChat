# coding: utf-8

import time
import json

def save_mongo(data,
                host=None,
                port=None,
                name=None,
                password="",
                dbname=None,
                collname=None):
    HOST = "localhost"
    PORT = 27017

    host = HOST if host is None else host
    port = PORT if port is None else port

    assert isinstance(host, str)
    assert isinstance(name, str)
    assert isinstance(password, str)
    assert isinstance(dbname, str)        
    assert isinstance(collname, str)

    if not isinstance(port, int):
        raise TypeError("port must be an instance of int")

    from pymongo import MongoClient
    # 连接数据库，一次性插入数据
    client = MongoClient(host, port)
    db_auth = client.admin
    db_auth.authenticate(name, password)
    coll = client[dbname][collname]
    coll.insert_many(data)

def save_json(fname, data):
    assert isinstance(fname, str)

    if ".json" not in fname:
        raise IOError("fname must be json", fname)
    with open(fname, "ab") as f:
        for item in data:
            #text = item
            text = json.dumps(dict(item),ensure_ascii=False)+'\n'
            f.write(text.encode('utf-8'))
        print('writeOK')