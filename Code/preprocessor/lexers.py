"""
  Contains Lexers that generate tokens that can be used for parsing abstracts. 
  The lexers are based on Pygments Lexers.
  Also creates a couple of helper fuctions that ease token generation
"""

from pygments.lexer import RegexLexer, include, bygroups, using
from pygments.token import Punctuation, Text, Comment, Keyword, Name, String, \
         Generic, Operator, Number, Whitespace, Literal, Token

Stopword = Token.Stopword
Equation = Token.Equation
Word = Token.Word
SpecialCharacter = Token.SpecialCharacter

class EnglishLexer(RegexLexer):
  """ 
    Lexer for English Language
  """

  name = "English Words"
  
  tokens = {
      'root': [
        (r'[,\.;\:\'\"\?\-\(\)\[\]\/`\*\+\|=><#\~@\\]', Punctuation),
        (r'\\', SpecialCharacter),
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
        if(t[0] is not Whitespace):
          l.append(t)

          # some weird unicode character gets through, this hack takes care of it
          if(t[0] is Token.Text):
            for t1 in el.get_tokens(t[1][1:]):
              if(t1[0] is not Whitespace):
                l.append(t1)
    else:
      l.append(token)
  return l


def tokenize_list(l, col, verbose=True):
  """
    Takes a 2D list and a col to tokenize in the list and returns a new list 
    that is a mirror of the argument list except the col column is replaced 
    with tokenized versions of the strings in the argument list. 
  """
  t = [] 
  i = 1 
  only_two = len(l[1])  ==  2
  for row in l: 
    if i % 1000 == 0 and verbose: print "Tokenized " + str(i)

    if only_two:
      t.append([get_tokens(row[col]), row[0] if col > 0 else row[1]])
    else:
      t.append([get_tokens(row[col]), row[:col] + row[col +1:]])
    i = i + 1 
  return t
