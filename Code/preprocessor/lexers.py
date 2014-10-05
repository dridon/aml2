"""
  Contains Lexers that generate tokens that can be used for parsing abstracts. 
  The lexers are based on Pygments Lexers.
  Also creates a couple of helper fuctions that ease token generation
"""

from pygments.lexer import RegexLexer, include, bygroups, using
from pygments.token import Punctuation, Text, Comment, Keyword, Name, String, \
         Generic, Operator, Number, Whitespace, Literal, Token
import StringIO
from stemming.porter2 import stem as stemming

Stopword = Token.Stopword
Equation = Token.Equation
Word = Token.Word
SpecialCharacter = Token.SpecialCharacter

stop_words = ["a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your"]
def get_stop_words_regex(): 
  s = StringIO.StringIO() 

  sws = [] 
  for w in stop_words: 
    sws.append(w.lower()) 
    sws.append(w.upper()) 
    sws.append(w.capitalize())
    if w not in sws: sws.append(w)

  for i in range(len(sws)):
    w = sws[i]
    s.write("\\s" + w + "\\s" + "|")
    s.write(w + "\\s" + "|")

    if i == len(sws) - 1:
      s.write("\\s" + w)
    else: 
      s.write("\\s" + w + "|")
  return s.getvalue()
swreg = get_stop_words_regex()

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
        # (r'\sthe\s|the\s|\sthe|\sof\s|of\s|\sof|\sin\s|in\s|\sin|\sand\s|and\s|\sand|\sto\s|to\s|\sto|\swe\s|we\s|\swe|\sis\s|is\s|\sis|\sfor\s|for\s|\sfor|\sthat\s|that\s|\sthat|\sthis\s|this\s|\sthis|\sare\s|are\s|\sare|\swith\s|with\s|\swith|\son\s|on\s|\son|\sby\s|by\s|\sby|\sas\s|as\s|\sas|\san\s|an\s|\san|\swhich\s|which\s|\swhich|\sbe\s|be\s|\sbe|\sour\s|our\s|\sour|\sit\s|it\s|\sit|\scan\s|can\s|\scan|\sfrom\s|from\s|\sfrom|\shas\s|has\s|\shas|\shave\s|have\s|\shave', Stopword),
        (swreg, Stopword),
        (r'\w+', Word),
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
def stem_token(t): 
  if t[0] is Word:
    print (stemming(t[1]))
    return (t[0], stemming(t[1]))
  else:
    return t

def get_tokens(s, stem = False):
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
          if stem:
            l.append(stem_token(t))
          else:
            l.append(t)

          # some weird unicode character gets through, this hack takes care of it
          if(t[0] is Token.Text):
            for t1 in el.get_tokens(t[1][1:]):
              if(t1[0] is not Whitespace):
                if stem:
                  l.append(stem_token(t1))
                else:
                  l.append(t1)
    else:
      l.append(token)
  return l


def tokenize_list(l, col, verbose=True, stem=False):
  """
    Takes a 2D list and a col to tokenize in the list and returns a new list 
    that is a mirror of the argument list except the col column is replaced 
    with tokenized versions of the strings in the argument list. 
  """
  t = [] 
  i = 1 
  only_two = len(l[1])  ==  2
  print "lexing(generating tokens)..." 
  for row in l: 
    if i % 1000 == 0 and verbose: print "\tcompleted " + str(i) + " samples"

    if only_two:
      t.append([get_tokens(row[col], stem), row[0] if col > 0 else row[1]])
    else:
      t.append([get_tokens(row[col], stem), row[:col] + row[col +1:]])
    i = i + 1 
  return t
