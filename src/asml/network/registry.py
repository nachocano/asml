from asml.autogen.services import RegistryService
from asml.autogen.services.ttypes import *
from client import Client

class RegistryClient(Client):
  def __init__(self, address):
    Client.__init__(self, address)

  def create_client(self, protocol):
    return RegistryService.Client(protocol)

  def reg(self, comp_type, address):
    client, transport = self.open()
    print 'register component type %s with address %s' % (comp_type, address)
    addresses = client.reg(comp_type, address)
    self.close(transport)
    return addresses

  def unreg(self, comp_type, address):
    client, transport = self.open()
    print 'unregister component type %s with address %s' % (comp_type, address)
    addresses = client.unreg(comp_type, address)
    self.close(transport)
    return addresses