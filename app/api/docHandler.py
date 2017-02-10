import json
import string
from app import log
from app.database import redis_db
from app.util.stringUtil import preProcess

LOG = log.get_logger()

def postDocument(result_json, doc_index):
    try:
        db = redis_db.RedisStorageEngine()
        r = db.connection()
    except Exception as ex:
        print ex

    """If the doc_index already exists, then this is a update post, remove doc_index from index first"""
    if (r.exists(doc_index)):
        origin_doc = r.get(doc_index).replace("u'",'"')
        origin_doc = origin_doc.replace("'",'"')
        documentBody = json.loads(origin_doc, encoding='utf-8')

        """update document index"""
        tokens = documentBody['message'].split(" ")
        for token in tokens:
            r.srem(token, doc_index)

    """Add/update document"""
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
    """
    When deleting document, two things need to update:
    1. delete doc_index with the mapping to document itself
    2. update the search index and remove the doc_index under the mapping keyword
    """
    try:
        db = redis_db.RedisStorageEngine()
        r = db.connection()
    except Exception as ex:
        print ex

    if (r.exists(doc_index)):
        result_json = r.get(doc_index).replace("u'",'"')
        result_json = result_json.replace("'",'"')
        documentBody = json.loads(result_json, encoding='utf-8')

        """update document index"""
        tokens = documentBody['message'].split(" ")
        for token in tokens:
            r.srem(token, doc_index)

            """delete document itself"""
            r.delete(doc_index)
    else:
        LOG.warning("doc_index: " + doc_index + " does not exists")
