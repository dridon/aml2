"""
  Contains filters for clearing out tokens 
"""

from pygments.token import Token 
import lexers as lx

def words(v): 
  return v[0] == Token.Word

def punctuations(v):
  return v[0] == Token.Punctuation

def stop_words(v): 
  return v[0] == Token.Stopword

def lt_three_chars(v): 
  return len(v[1]) < 3
