import abc
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class Client:
  __metaclass__ = abc.ABCMeta
  
  def __init__(self, addresses):
    self._clients = {}
    self._transports = {}
    self._protocols = {}
    try:
      for address in addresses.split(','):
        host, port = address.split(':')
        port = int(port)
        transport = TSocket.TSocket(host, port)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self._transports[(host, port)] = transport
        self._protocols[(host, port)] = protocol
    except Thrift.TException as tx:
      print(('client exc: %s' % (tx.message)))

  def open(self):
    for key in self._protocols:
      self._clients[key] = self.create_client(self._protocols[key])
      try:
        self._transports[key].open()
        print 'connected to %s' % str(key)
      except Thrift.TException as tx:
        print(('client exc: %s' % (tx.message)))

  def close():
    for key in self._transports:
      try:
        transport = self._transports[key]
        print 'closing connection to %s' % str(key)
        transport.close()
      except Thrift.TException as tx:
        print(('client exc: %s' % (tx.message)))

  def get_clients(self):
    return self._clients

  @abc.abstractmethod
  def create_client(self, protocol):
    return