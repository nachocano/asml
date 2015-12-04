from criteo import CriteoParser

class ParserFactory:

  @classmethod
  def new_parser(cls, parser):
    if parser == 'criteo':
      return CriteoParser()
    else:
      raise ValueException('invalid parser %s' % value)