from asml.autogen.services import NotificationService
from asml.autogen.services.ttypes import *
from client import Client

class NotificationClient(Client):
  def __init__(self, module_properties):
    Client.__init__(self, module_properties['predictor_addresses'])

  def create_client(self, protocol):
    return NotificationService.Client(protocol)

  def best_model(self, id, timestamp):
    clients = self.get_clients()
    for key in clients:
      print 'notifying of best model to %s' % str(key)
      client[key].best_model(id, timestamp)