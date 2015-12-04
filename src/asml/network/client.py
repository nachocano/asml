from asml.autogen.asml import StreamService
from asml.autogen.asml.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class StreamClient:
  def __init__(self, module_properties):
    self._connections = {}
    for address in module_properties['downstream_addresses'].split(','):
      host, port = address.split(':')
      port = int(port)
      self._connections[(host, port)] = self.open(host, port)

  def open(self, host, port):
    try:
      # Make socket
      transport = TSocket.TSocket(host, port)
      # Buffering is critical. Raw sockets are very slow
      transport = TTransport.TBufferedTransport(transport)
      # Wrap in a protocol
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      # Create a client to use the protocol encoder
      client = StreamService.Client(protocol)
      # Connect!
      transport.open()
      print 'connected to server in %s:%s' % (host, port)
      return transport, client

    except Thrift.TException as tx:
      print(('streamclient exc: %s' % (tx.message)))
      #exit(1)

  def emit(self, data):
    for conn in self._connections:
      client = self._connections[conn][1]
      print 'emitting data to %s' % str(conn)
      client.emit(data)

  def close():
    for conn in self._connections:
      trans = self._connections[conn][0]
      print 'closing connection to %s' % str(conn)
      transport.close()
