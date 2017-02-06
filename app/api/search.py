# search.py

import falcon
import string
import json
from . import redis_db
from app.util.stringUtil import preProcess

class SearchResource(object):

    def __init__(self, db):
        self.db = db

    # This function handles GET reuqests
    def on_get(self, req, resp):
        try:
            db = redis_db.RedisStorageEngine()
            r = db.connection()
        except Exception as ex:
            print ex

        if req.get_param("q"):
            keywords = req.get_param("q").split(" ")
            counter = 1
            result = set()
            for keyword in keywords:
                """
                Strip punctuation from string and convert into lower case.
                otherwise 'Do' and 'do' will be 2 different keywords.
                """
                keyword = preProcess(keyword)
                if counter == 1:
                    """SMEMBERS returns all the members of the set value stored at key."""
                    result = r.smembers(keyword)
                else:
                    """use set intersection to return the list of document IDs that match all the keywords"""
                    result = result.intersection(r.smembers(keyword))
                counter += 1

            resp.body = json.dumps(list(result))
            resp.status = falcon.HTTP_200  # This is the default status
