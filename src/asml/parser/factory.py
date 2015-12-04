from criteo import CriteoParser

class ParserFactory:

  @classmethod
  def new_parser(cls, parser):
    if parser == 'criteo':
      return CriteoParser()
    raise ValueException('invalid parser %s' % value)