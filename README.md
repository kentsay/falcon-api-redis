## Falcon REST API with Redis - Simple Text search service

Simple text search service with using Falcon web framework and Redis.

Falcon is a minimalist WSGI library for building speedy web APIs and app backends. More information can be found [here](http://falcon.readthedocs.io/en/stable/index.html).

### Service features
The simple text search service are required to have the following features:

* The service should hold document in redis (or in memory)
* Documents are just text (no fields to parse)
* `POST /document/XXX` Indexs a document with ID XXX
* `GET /document/XXX` Returns the document with ID XXX
* `DELETE /document/XXX` Deletes document with ID XXX
* `GET /search?q={keyword}` Returns the list of documents IDs that match the given keyword (single word search)
* `GET /search?q={keyword1 keyword2 ... keywordN}` Returns the list of document IDs that match all the keywords

The service should be optimized for search speed and should be able to handle thousands of documents.

### Simple architecture
In order to achieve the optimization performance, we use RQ ([Redis Queue](http://python-rq.org/)) to handle write request(POST, DELETE, etc). RQ is a simple Python library for queueing jobs and processing them in the background with workers.

If you have enough resource and want to scale out your service, you can use a Nginx load balancer in front, and forward all READ quest to one server, and all the WRITE request to another.

### Requirements

This project uses [virtualenv](https://virtualenv.pypa.io/en/stable/) as isolated Python environment for installation and running. Therefore, [virtualenv](https://virtualenv.pypa.io/en/stable/) must be installed.

### Installation

Install all the python module dependencies in requirements.txt
```
  ./install.sh
```

Start server
```
  ./bin/run.sh start
```

Start workers
```
  python worker.py
```

### Usage

Create document
- Request
```shell
curl -XPOST http://localhost:8000/document/1 -H "Content-Type: application/json" -d '{
 "message": "Meet people from various countries, cultures and diverse
backgrounds. We work in interdisciplinary teams to innovate and
open fundamentally new ways to deliver product insurances."
}'
```

- Response
```json
{
"message": "Meet people from various countries, cultures and diverse
backgrounds. We work in interdisciplinary teams to innovate and
open fundamentally new ways to deliver product insurances."
}
```

GET document
- Request
```shell
curl -XGET http://localhost:8000/document/1
```

- Response
```json
{
"message": "Meet people from various countries, cultures and diverse
backgrounds. We work in interdisciplinary teams to innovate and
open fundamentally new ways to deliver product insurances."
}
```

DELETE document
- Request
```shell
curl -XDELETE http://localhost:8000/document/1
```

- Response
```json
{}
```

Search documents ID by keyword
- Request
```shell
curl -XGET http://localhost:8000/search?q=people cultures
```

- Response
```json
{"1", "2"}
```
