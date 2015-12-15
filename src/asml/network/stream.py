from asml.autogen.services import StreamService
from asml.autogen.services.ttypes import *
from client import Client


class StreamClient(Client):
  def __init__(self, address):
    Client.__init__(self, address)

  def create_client(self, protocol):
    return StreamService.Client(protocol)

  def emit(self, data):
    client, transport = self.open()
    print 'emit to %s' % self._address
    client.emit(data)
    self.close(transport)

  def notify(self, addresses):
    client, transport = self.open()
    print 'notify to %s' % self._address
    client.notify(addresses)
    self.close(transport)
