import threading
from asml.autogen.services import RegistryService
from asml.autogen.services.ttypes import ComponentType
from asml.network.stream import StreamClient
from asml.network.server import Server
from collections import defaultdict
import logging

class RegistryHandler:
  def __init__(self):
    self._lock = threading.Lock()
    self._deployer = None
    self._featgen = None
    self._ds = None
    self._learners = {}


  # you register the component, and piggyback the addresses of the components
  # you should connect to
  def reg(self, comp_type, address):
    print 'register %s at %s' % (comp_type, address)
    try:
      if comp_type == ComponentType.DATASTREAM:
        self._ds = address
        return [self._featgen]
      elif comp_type == ComponentType.FEATGEN:
        self._featgen = address
        return self._learners
      elif comp_type == ComponentType.LEARNER:
        # need to notify the deployer of how many learners he should wait for
        with self._lock:
          self._learners[address] = True
        self._notify(self._deployer, self._learners.keys())
        # also tell the feature generator, to contact those learners
        if self._featgen:
          self._notify(self._featgen, self._learners.keys())
        return [self._deployer]
      elif comp_type == ComponentType.DEPLOYER:
        self._deployer = address
        return []
      else:
        raise ValueError("invalid component type")
    except Exception, ex:
      print 'exc registering %s at %s' % (comp_type, address)

 
  def unreg(self, comp_type, address):
    print 'unregister %s at %s' % (comp_type, address)
    try:
      if comp_type == ComponentType.LEARNER:
        updated = False
        with self._lock:
          if self._learners.has_key(address):
            del self._learners[address]
            updated = True
            print 'unregistered %s at %s' % (comp_type, address)
        # ugly stuff until I fix the feature generator, not to even communicate to this...
        if updated:
          self._notify(self._deployer, self._learners.keys())
        return self._learners.keys()
      else:
        raise ValueError("only support %s failure, not from %s" % (ComponentType.LEARNER, comp_type))
    except Exception, ex:
      print 'exc unregistering %s at %s' % (comp_type, address)


  def _notify(self, to, addresses):
    try:
      client = StreamClient(to)
      client.notify(addresses)
    except Exception, ex:
      print 'exc notifying %s' % to
  
class Registry:
  def __init__(self, module_properties):
    self._processor = RegistryService.Processor(RegistryHandler())
    self._registry_server = Server(self._processor, module_properties['server_port'], module_properties['multi_threading'])

  def run(self):
    self._registry_server.start()
