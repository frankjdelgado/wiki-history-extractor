from pymongo import MongoClient

class RevisionDB(object):
    client = MongoClient()
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
    def find_last(cls):
        cursor= cls.db.revisions.find({},{'revid':1 , '_id':0})
        cursor = cursor.sort('revid', -1).limit(1)
        return cursor

    @classmethod
    def remove(cls):
        revisions = cls.db.revisions.remove({})
        return revisions

