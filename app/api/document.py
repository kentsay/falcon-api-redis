#document.py

import falcon
import string
import json
from rq import Queue
from rq.job import Job
from writer import postDocument, delDocument

"""
Todo list:
3. modify redis indexing for query value and get key
4. redix better way to handle set & get (mset, etc)
5. api error handling
"""

class DocumentResource(object):

    def __init__(self, db):
        self.db = db

    # This function handles GET reuqests
    def on_get(self, req, resp, doc_index):
        try:
            r = self.db.connection()
        except Exception as ex:
            print ex

        result = r.get(doc_index)
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

    # This function handles POST reuqests
    def on_post(self, req, resp, doc_index):
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

        """
        Enqueueing write request as jobs into document_write queue
        and processing them in the background with workers.
        """
        q = Queue('document_write', connection=self.db.connection())
        job = q.enqueue_call(
            func=postDocument, args=(result_json, doc_index), result_ttl=5000
        )
        print(job.get_id())

        resp.status = falcon.HTTP_202
        resp.body = json.dumps(result_json, encoding='utf-8')


    # This function handles DELETE reuqests
    def on_delete(self, req, resp, doc_index):
        """
        Enqueueing write request as jobs into document_delete queue
        and processing them in the background with workers.
        """
        q = Queue('document_delete', connection=self.db.connection())
        job = q.enqueue_call(
            func=delDocument, args=(doc_index,), result_ttl=5000
        )
        print(job.get_id())
