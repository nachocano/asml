from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class Server:
  def __init__(self, processor, portno, multi_threading):
    self._portno = portno
    try:
      self._transport = TSocket.TServerSocket(port=self._portno)
      tfactory = TTransport.TBufferedTransportFactory()
      pfactory = TBinaryProtocol.TBinaryProtocolFactory()
      if multi_threading:
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
