"""
  Contains maps that can be used to transform strings
"""

from stemming.porter2 import stem

def to_lower(v):
  return str(v).lower() 

def stem(v): 
  return stem(str(v))

def no_back_slash(v): 
  return v.replace("\\", "")
