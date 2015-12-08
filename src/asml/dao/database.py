import psycopg2
from asml.util.utils import Utils

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
    cur.execute(self._sql['save_model'], {'timestamp': long(timestamp), 'id': id, 
                'data': Utils.serialize(model), 'metric' : float(metric)})
    self._conn.commit()
    cur.close()

  def get_model(self, id, timestamp):
    print 'retrieving model %s at %s' % (id, timestamp)
    cur = self._conn.cursor()
    cur.execute(self._sql['get_model'], {'timestamp' : long(timestamp), 'id' : id})
    tupl = cur.fetchone()
    model = None
    if tupl:
      model = Utils.deserialize(tupl[0])
    cur.close()
    return model

