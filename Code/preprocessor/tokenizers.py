import re

class Tokenizer:
  """ 
    Generates tokens for given string input formats
  """
  def __init__(self, delimiter=None):
    self.delimiter = " " if delimiter is None else delimiter

  def tokenize(self, s): 
    """
      Tokenizes a string simply by splitting it
    """
    return s.split(self.delimiter)

  def tokenize_list(self, l, cols): 
    """ 
      Tokenizes specific columns in a list 
    """
    return [[self.tokenize(row[i]) if i in cols else row[i] for i in range(len(row))] for row in l]


class Equation_Tokenizer(Tokenizer): 
  """ 
    Generates tokens for given string input formats but ignores delimiter inside
    Equations
  """
  def __init__(self, delimiter=None):
    Tokenizer.__init__(self, delimiter)

  def tokenize(self, s): 
    """ 
      Tokenizes specific columns in a list 
    """
    p = '''[''' + self.delimiter + '''](?=(?:[^\$]|\$[^\$]*\$)*$)'''
    return re.compile(p).split(s)
