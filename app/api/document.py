#document.py

import falcon
import string
import json

documents_dict = {}
documents_index = []

class DocumentResource(object):

    def __init__(self, db):
        self.db = db

    def on_post(self, req, resp, doc_index):
        """Handles POST request"""
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Error',
                ex.message)
        try:
            result_json = json.loads(raw_json, encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Malformed JSON',
                'Could not decode the request body. The JSON was incorrect.')

        try:
            r = self.db.connection()
        except Exception as ex:
            print ex

        key = doc_index
        r.set(key, result_json)
        documents_index.append(key)

        key_word = result_json['message'].split(" ")
        for w in key_word:
            # strip punctuation from string and convert into lower case
            # otherwise 'Do' and 'do' will be 2 different keywords
            w = w.strip(string.punctuation).lower()
            if documents_dict.has_key(w):
                documents_dict[w].append(key)
            else:
                documents_dict[w] = [];
                documents_dict[w].append(key)

        resp.status = falcon.HTTP_202
        resp.body = json.dumps(result_json, encoding='utf-8')

    def on_get(self, req, resp, doc_index):
        """Handles GET requests"""
        try:
            r = self.db.connection()
        except Exception as ex:
            print ex

        result = r.get(doc_index)
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200


    def on_delete(self, req, resp, doc_index):
        """Handles DEL requests"""
        try:
            r = self.db.connection()
        except Exception as ex:
            print ex

        r.delete(doc_index)
