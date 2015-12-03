from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class StreamServer:
  def __init__(self, module_properties, processor):
    try:
      self._transport = TSocket.TServerSocket(port=module_properties['server_port'])
      tfactory = TTransport.TBufferedTransportFactory()
      pfactory = TBinaryProtocol.TBinaryProtocolFactory()
      self._server = TServer.TSimpleServer(processor, self._transport, tfactory, pfactory)
      print('starting the server...')
      self._server.serve()
    except (KeyboardInterrupt, SystemExit):
       print "quitting from keyboard interrupt"
       self._transport.close()
    except Exception, ex:
      print(('streamserver exc: %s' % (ex.message)))

  def shutdown(self):
    print('stopping the service...')
    self._server.stop()
