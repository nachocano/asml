from criteo import CriteoParser
from kdd import KddParser

class ParserFactory:

  @classmethod
  def new_parser(cls, module_properties):
    parser = module_properties['parser']
    if parser == 'criteo':
      return CriteoParser(module_properties)
    elif parser == 'kdd':
      return KddParser(module_properties)
    else:
      raise ValueError('invalid parser %s' % value)