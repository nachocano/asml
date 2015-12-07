from asml.autogen.services import StreamService
from asml.autogen.services.ttypes import *
from client import Client


class StreamClient(Client):
  def __init__(self, module_properties):
    Client.__init__(self, module_properties['downstream_addresses'])

  def create_client(self, protocol):
    return StreamService.Client(protocol)

  def emit(self, data):
    clients = self.get_clients()
    for key in clients:
      print 'emitting data to %s' % str(key)
      clients[key].emit(data)