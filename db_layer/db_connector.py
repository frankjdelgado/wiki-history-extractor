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
