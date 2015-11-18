
class Predictor:
  def __init__(self, app_properties, cache, dao, evaluator, child):
    self._batch_size = app_properties['batch_size']
    self._deploy_batch_size = app_properties['deploy_batch_size']
    self._cache = cache
    self._dao = dao
    self._evaluator = evaluator
    self._child = child

  def _save_model(self, i):
    self._dao.save_model(i, self._name, Serializer.serialize(self._clf))

  def _get_model(self, i):
    pass#self._dao.save_model(i, self._name, Serializer.serialize(self._clf))

  def next(self):
    for i, (X, y) in enumerate(self._child.next()):
      if self._warmup(i):
        pass
        # do not predict, models are being trained...
      else:
        # predict
        model = self._get_model()
        predictions = model.predict(X)
        yield i, y, predictions

