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

### Usage
