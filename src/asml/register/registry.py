import threading
from asml.autogen.services import RegistryService
from asml.autogen.services.ttypes import ComponentType
from asml.network.server import Server
from collections import defaultdict
import logging

class RegistryHandler:
  def __init__(self):
    self._lock = threading.Lock()
    self._deployer = []
    self._featgen = []
    self._ds = []
    self._learners = []


  def reg(self, comp_type, address):
    print 'register %s at %s' % (comp_type, address)
    if comp_type == ComponentType.DATASTREAM:
      self._ds = [address]
      return self._featgen
    elif comp_type == ComponentType.FEATGEN:
      self._featgen = [address]
      return self._learners
    elif comp_type == ComponentType.LEARNER:
      self._learners.append(address)
      return self._deployer
    elif comp_type == ComponentType.DEPLOYER:
      self._deployer = [address]
      return []
    else:
      raise ValueError("invalid component type")

 
  def unreg(self, comp_type, address):
    print 'unregister %s at %s' % (comp_type, address)

  
class Registry:
  def __init__(self, module_properties):
    self._processor = RegistryService.Processor(RegistryHandler())
    self._registry_server = Server(self._processor, module_properties['server_port'], module_properties['multi_threading'])

  def run(self):
    self._registry_server.start()
