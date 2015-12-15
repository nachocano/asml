from asml.autogen.services import StreamService
from asml.network.stream import StreamClient
from asml.network.server import Server
from asml.parser.factory import ParserFactory

class FeatureGeneratorHandler:
  def __init__(self, client, parser, dao, historical_batches):
    self._stream_client = client
    self._parser = parser
    self._dao = dao
    self._historical_batches = historical_batches
    self._batches = 0

  def emit(self, data):
    try:
      examples = self._parser.parse_raw(data)
      self._dao.save_examples(examples[1:])
      self._batches += 1
      # TODO put this in another thread
      if self._batches > self._historical_batches:
        batch_size = len(data)
        # get last timestamp of batch
        last_timestamp = long(examples[-1].split(' ')[0])
        # max timestamp to delete
        max_timestamp = last_timestamp - self._historical_batches * batch_size
        self._dao.delete_examples(max_timestamp)
        self._batches = 0
      self._stream_client.emit(examples, multithreaded=True)
    except Exception, ex:
      print 'ex %s' % ex.message

class FeatureGenerator:
  def __init__(self, dao, module_properties):
    self._dao = dao
    self._parser = ParserFactory.new_parser(module_properties)
    self._historical_batches = module_properties['historical_batches']
    self._stream_client = StreamClient(module_properties)
    self._processor = StreamService.Processor(FeatureGeneratorHandler(self._stream_client, self._parser, 
                                              self._dao, self._historical_batches))
    self._stream_server = Server(self._processor, module_properties['server_port'], module_properties['multi_threading'])

  def run(self):
    self._stream_client.open()
    self._stream_server.start()
