import json
import string
from app.database import redis_db
from app.util.stringUtil import preProcess

def postDocument(result_json, doc_index):
    try:
        db = redis_db.RedisStorageEngine()
        r = db.connection()
    except Exception as ex:
        print ex

    r.set(doc_index, result_json)

    """
    Since we cannot query on document of a document index, you have to manually build and maintain document indexes.
    """
    tokens = result_json['message'].split(" ")
    for token in tokens:
        """
        Strip punctuation from string and convert into lower case.
        otherwise 'Do' and 'do' will be 2 different keywords.
        """
        token = preProcess(token)
        """
        SADD: Add the specified members to the set stored at key. Specified members that are already a member of this set are ignored.
        """
        r.sadd(token, doc_index)

def delDocument(doc_index):
    try:
        db = redis_db.RedisStorageEngine()
        r = db.connection()
    except Exception as ex:
        print ex

    r.delete(doc_index)
