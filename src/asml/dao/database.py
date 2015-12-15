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

  def save_model(self, id, timestamp, model):
    print 'saving model %s' % id
    cur = self._conn.cursor()
    cur.execute(self._sql['save_model'], {'id': id, 'timestamp': timestamp, 'data': Utils.serialize(model)})
    self._conn.commit()
    cur.close()

  def update_model(self, id, timestamp, model):
    print 'updating model %s' % id
    cur = self._conn.cursor()
    cur.execute(self._sql['update_model'], {'id': id, 'timestamp': timestamp, 'data': Utils.serialize(model), 'cond' : id})
    self._conn.commit()
    cur.close()    

  def get_model(self, id):
    print 'retrieving model %s' % id
    cur = self._conn.cursor()
    cur.execute(self._sql['get_model'], {'id' : id})
    tupl = cur.fetchone()
    model = None
    timestamp = None
    if tupl:
     timestamp = tupl[0]
     model = Utils.deserialize(tupl[1])
     print 'retrieved model %s' % id
    else:
      print 'not retrieved model %s' % id
    cur.close()
    return model, timestamp

  def save_examples(self, examples):
    print 'saving examples'
    cur = self._conn.cursor()
    args = []
    for example in examples:
      timestamp = example.split(' ')[0]
      args.append((timestamp, example))
    records_list_template = ','.join(['%s'] * len(args))
    insert_query = self._sql['save_examples'].format(records_list_template)
    cur.execute(insert_query, args)
    self._conn.commit()
    cur.close()

  def get_examples(self):
    pass

  def delete_examples(self, timestamp):
    print 'deleting examples prior to %s' % timestamp
    cur = self._conn.cursor()
    cur.execute(self._sql['delete_examples'], {'timestamp' : timestamp})
    self._conn.commit()
    cur.close()
