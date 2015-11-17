import base64
import psycopg2
try:
  import cPickle as pickle
except:
  import pickle

class DB:
  def __init__(self, app_properties, conn_properties, sql_statements):
    self._name = app_properties['name']
    self._sql = sql_statements
    try:
      self._conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                            (conn_properties['dbname'], conn_properties['user'], 
                              conn_properties['host'], conn_properties['password']))
      print 'Connected to database...'
    except psycopg2.Error, e:
      raise Exception("Unable to connect to the database")


  def save_model(self, epoch, name, clf):
    print 'saving model %s' % epoch
    cur = self._conn.cursor()
    encoded_model = base64.b64encode(pickle.dumps(clf, pickle.HIGHEST_PROTOCOL))
    cur.execute(self._sql['save_model'], (epoch, self._name, encoded_model))
    self._conn.commit()


