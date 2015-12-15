import abc
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from asml.util.utils import Utils


class Client:
  __metaclass__ = abc.ABCMeta
  
  def __init__(self, address):
    host, port = Utils.get_address_components(address)
    self._host = host
    self._port = port
    self._address = address

  def open(self):
    transport = TSocket.TSocket(self._host, self._port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = self.create_client(protocol)
    transport.open()
    #print 'connected to %s' % self._address
    return client, transport

  def close(self, transport):
    #print 'closing connection to %s' % self._address
    transport.close()

  @abc.abstractmethod
  def create_client(self, protocol):
    return

  def get_address(self):
    return self._address