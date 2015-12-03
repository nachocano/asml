
class FeatureGeneratorHandler:
  def __init__(self, client):
    self._stream_client = client

  def emit(self, data):
    print(data)
    #self._stream_client.emit(data)