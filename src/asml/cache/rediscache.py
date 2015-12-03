from redis import Redis

class RedisCache:
  def __init__(self, conn_properties):
    self._key_prefix = conn_properties['redis_key_prefix']
    try:
      self._cache = Redis(conn_properties['redis_host'])
      print 'Connected to redis...'
    except Exception:
      raise Exception("Unable to connect to the redis")

  def set_value():
    pass

  def get_value():
    pass

