"""
  Contains Lexers that generate tokens that can be used for parsing abstracts. 
  The lexers are based on Pygments Lexers.
  Also creates a couple of helper fuctions that ease token generation
"""

from pygments.lexer import RegexLexer, include, bygroups, using
from pygments.token import Punctuation, Text, Comment, Keyword, Name, String, \
         Generic, Operator, Number, Whitespace, Literal, Token

class EnglishLexer(RegexLexer):
  """ 
    Lexer for English Language
  """

  name = "English Words"
  Stopword = Token.Stopword
  Word = Token.Word
  
  tokens = {
      'root': [
        (r'[,\.;\:\'\"\?\-]', Punctuation),
        (r'\s', Whitespace),
        (r'\w+', Word),
        (r'the|with|to|for|a|we', Stopword),
        (r'[^,!\.;:\'\"\?]+', Text),
        ],
      }

class AbstractsLexer(RegexLexer):
  """ 
    Lexer for abstracts in dataset
    Based on TexLexer provided by Pygments
  """

  name = "Abstract"

  Equation = Token.Equation
  
  tokens = {
      'general': [
        (r'%.*?\n', Comment),
        (r'[{}]', Name.Builtin),
        (r'[&_^]', Name.Builtin),
        ],
      'root': [
        (r'\\\[', Equation, 'displaymath'),
        (r'\\\(', Equation, 'inlinemath'),
        (r'\$\$', Equation, 'displaymath'),
        (r'\$', Equation, 'inlinemath'),
        (r'\\([a-zA-Z]+|.)', Keyword, 'command'),
        include('general'),
        (r'[^\\$%&_^{}]+', Text),
        ],
      'math': [
        (r'\\([a-zA-Z]+|.)', Name.Variable),
        include('general'),
        (r'[0-9]+', Number),
        (r'[-=!+*/()\[\]]', Operator),
        (r'[^=!+*/()\[\]\\$%&_^{}0-9-]+', Text),
        ],
      'inlinemath': [
        (r'\\\)', Equation),
        (r'\$', Equation),
        include('math'),
        ],
      'displaymath': [
        (r'\\\]', Equation),
        (r'\$\$', Equation),
        (r'\$', Name.Builtin),
        include('math'),
        ],
      'command': [
        (r'\[.*?\]', Name.Attribute),
        (r'\*', Keyword),
        (r'', Text, '#pop'),
        ],
      }

def get_tokens(s):
  """
    Generates tokens for a given string
  """
  al = AbstractsLexer() 
  el = EnglishLexer()

  l = []
  for token in al.get_tokens(s): 
    if token[0] is Token.Text:
      for t in el.get_tokens(token[1]):
        l.append(t)
    else:
      l.append(token)
  return l


def tokenize_list(l, col):
  """
    Takes a 2D list and a col to tokenize in the list and returns a new list 
    that is a mirror of the argument list except the col column is replaced 
    with tokenized versions of the strings in the argument list. 
  """
  t = [] 
  i = 1 
  for row in l: 
    if i % 1000 == 0 : print "Tokenized " + str(i)
    t.append([get_tokens(row[col]), row[:col] + row[col +1:]])
    i = i + 1 
  return t
