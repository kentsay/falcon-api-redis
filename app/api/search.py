# search.py

import falcon
import string
import document
import json

class SearchResource(object):

    def __init__(self, db):
        self.db = db

    def on_get(self, req, resp):
        """Handles GET requests"""
        intersect = []
        if req.get_param("q"):
            keywords = req.get_param("q").split(" ")
            counter = 1
            for keyword in keywords:
                if document.documents_dict.has_key(keyword):
                    # Returns the list of document IDs that match all the keywords
                    if counter == 1:
                        intersect = set(document.documents_dict[keyword]).intersection(set(document.documents_index))
                    else:
                        intersect = set(document.documents_dict[keyword]).intersection(set(intersect))
                        counter += 1

            resp.body = json.dumps(list(intersect))
            resp.status = falcon.HTTP_200  # This is the default status
