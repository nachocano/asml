from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class Server:
  def __init__(self, module_properties, processor):
    self._portno = module_properties['server_port']
    try:
      self._transport = TSocket.TServerSocket(port=self._portno)
      tfactory = TTransport.TBufferedTransportFactory()
      pfactory = TBinaryProtocol.TBinaryProtocolFactory()
      if module_properties['multi_threading']:
        self._server = TServer.TThreadedServer(processor, self._transport, tfactory, pfactory)
      else:
        self._server = TServer.TSimpleServer(processor, self._transport, tfactory, pfactory)
    except Exception, ex:
      print(('server exc: %s' % (ex.message)))

  def start(self):
    try:
      print('starting the server on port %s' % self._portno)
      self._server.serve()
    except (KeyboardInterrupt, SystemExit):
       print "quitting from keyboard interrupt"
       self._transport.close()
    except Exception, ex:
      print(('could not start server, server exc: %s' % (ex.message)))

  def stop(self):
    print('stopping the service...')
    self._server.stop()
