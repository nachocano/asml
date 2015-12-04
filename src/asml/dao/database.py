import psycopg2

class DB:
  def __init__(self, app_properties, conn_properties, sql_statements):
    self._sql = sql_statements
    try:
      self._conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                            (conn_properties['dbname'], conn_properties['user'], 
                              conn_properties['host'], conn_properties['password']))
      print 'Connected to database...'
    except psycopg2.Error, e:
      raise Exception("Unable to connect to the database")


  def save_model(self, timestamp, name, model, metric):
    print 'saving model %s' % timestamp
    cur = self._conn.cursor()
    cur.execute(self._sql['save_model'], (timestamp, name, model, metric))
    self._conn.commit()

