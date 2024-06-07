import redis

def initialize_redis():
    redis_client = redis.StrictRedis(host = 'localhost', port= 6379, db =0)
    return redis_client

redis_client = initialize_redis()