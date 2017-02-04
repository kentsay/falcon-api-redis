import redis

class RedisStorageEngine(object):
    def connection(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        r = redis.Redis(connection_pool=pool)
        return r
