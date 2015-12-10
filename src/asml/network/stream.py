from asml.autogen.services import StreamService
from asml.autogen.services.ttypes import *
from client import Client
from threading import Thread


class StreamClient(Client):
  def __init__(self, module_properties):
    Client.__init__(self, module_properties['downstream_addresses'])

  def create_client(self, protocol):
    return StreamService.Client(protocol)

  def _multi_threaded_emit(self, data):
    clients = self.get_clients()
    try:
      threads = []
      for key in clients:
        thread = Thread(target=self._do_emit, args=(clients[key], key, data))
        threads.append(thread)
      # start the threads
      print 'starting threads'
      for t in threads:
        t.start()
      # wait for completion
      print 'joining threads'
      for t in threads:
        t.join()
    except Exception, ex:
      print(('exc in multithread emit: %s' % (ex.message)))

  def _single_threaded_emit(self, data):
    clients = self.get_clients()
    for key in clients:
      try:
        print 'emitting data to %s' % str(key)
        clients[key].emit(data)
      except Exception, ex:
        print(('exc while emitting: %s' % (ex.message)))    

  def _do_emit(self, client, key, data):
      try:
        print 'emitting data to %s' % str(key)
        client.emit(data)
      except Exception, ex:
        print(('exc while emitting: %s' % (ex.message)))

  def emit(self, data, multithreaded=False):
    if multithreaded:
      self._multi_threaded_emit(data)
    else:
      self._single_threaded_emit(data)


