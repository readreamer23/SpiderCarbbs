#coding:utf-8
from random import choice
import requests
import time,random
import pymongo


client=pymongo.MongoClient('127.0.0.1',27017)
dbname='qichezhijia'

collectionname1='qichezhijia1'
collectionname2='qichezhijia2'
autohome_bbs_content='autohome_bbs_content'
koubei='koubei'

def insertMongo1(content):
    db=client[dbname]
    collection=db[collectionname1]
    collection.insert(content)
    client.close()

def insertMongo2(content):
    db=client[dbname]
    collection=db[collectionname2]
    collection.insert(content)
    client.close()
    
def insertMongoBBS(content):
    db=client[dbname]
    collection=db[autohome_bbs_content]
    collection.insert(content)
    client.close()    
    
def insertMongoKoubei(content):
    db=client[dbname]
    collection=db[koubei]
    result=collection.insert(content)
    client.close()
    return result     

def findByType(name,value):
    db=client[dbname]
    collection=db[collectionname1]
    query = { name: value }
    result = collection.find(query)
    return result


def groupbyType1(grouptype,grouptname):
    db=client[dbname]
    collection=db[collectionname1]
    pipe=[
                #{"$match":{"user":{"user":"user"}}},
                {"$group":{"_id":"$"+grouptype,grouptname:{"$sum":1}}}
                ]
    result = collection.aggregate(pipeline=pipe)
    return result
     

if __name__=='__main__':
    content={"test1":"test1"}
    insertMongo1(content)
    

