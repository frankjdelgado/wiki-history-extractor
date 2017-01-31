from pymongo import MongoClient
import json

class RevisionDB(object):
    
    # it is extracted the information of the database connection, located in the 'connection_data.json' file
    with open('connection_data.json') as json_data:
        data = json.load(json_data)

    host=data['host']
    port=data['port']
    username=data['username']
    password=data['password']
    client = MongoClient(host=host,port=port)
    if client.wiki_history_extractor.authenticate(username, password, mechanism='SCRAM-SHA-1') == True :
        db = client.wiki_history_extractor

    @classmethod
    def insert(cls, revisions):
        #Insert only if it does not exists
        for revision in revisions:
            cls.db.revisions.update({'revid': revision['revid']}, revision, upsert=True)

    @classmethod
    def find(cls):
        revisions = cls.db.revisions.find()
        return revisions

    @classmethod
    def count(cls,query):
        revisions = cls.db.revisions.find(query).count()
        print revisions

    @classmethod
    def find_last(cls):
        cursor= cls.db.revisions.find({},{'revid':1 , '_id':0})
        cursor = cursor.sort('revid', -1).limit(1)
        return cursor

    @classmethod
    def remove(cls):
        revisions = cls.db.revisions.remove({})
        return revisions

