import psycopg2

class DB:
  def __init__(self, db_properties, sql_statements):
    self._sql = sql_statements
    try:
      self._conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                            (db_properties['dbname'], db_properties['user'], 
                              db_properties['host'], db_properties['password']))
      print 'Connected to database...'
    except psycopg2.Error, e:
      raise Exception("Unable to connect to the database")
      exit(1)


  def save_model(self, timestamp, id, model, metric):
    print 'saving model %s at %s' % (id, timestamp)
    cur = self._conn.cursor()
    cur.execute(self._sql['save_model'], (long(timestamp), id, model, float(metric)))
    self._conn.commit()