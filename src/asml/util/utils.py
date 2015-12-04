import yaml

class Utils:

  @classmethod
  def read_properties(cls, fd):
    with open(fd) as f:
      return yaml.load(f)