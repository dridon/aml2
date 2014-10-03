"""
  Contains filters for clearing out tokens 
"""

import lexers

def words(v): 
  return v[0] == Token.Word

def punctuations(v):
  return v[0] == Token.Punctuation

def stop_words(v): 
  return v[0] == Token.Stopword

def gt_two_chars(v): 
  return len(v[1]) > 2
