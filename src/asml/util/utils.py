import yaml

class Utils:

  @classmethod
  def warmup(cls, warmup_batches, i):
    return warmup_batches > i

  @classmethod
  def read_properties(cls, fd):
    with open(fd) as f:
      return yaml.load(f)