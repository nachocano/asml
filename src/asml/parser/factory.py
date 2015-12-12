from criteo import CriteoParser

class ParserFactory:

  @classmethod
  def new_parser(cls, module_properties):
    parser = module_properties['parser']
    if parser == 'criteo':
      return CriteoParser(module_properties)
    else:
      raise ValueError('invalid parser %s' % value)