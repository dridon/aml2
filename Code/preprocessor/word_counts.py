"""
  A helper class to ease preprocessing
"""
from collections import OrderedDict

class WordCounter:
  raw_data = None
  word_counts = None 
  ordered_counts = None

  def __init__(self, data): 
    self.raw_data = data

  def load_word(self, w, d): 
    if w not in d: 
      d[w] = 0 
    d[w] = d[w] + 1 

  def get_word_counts(self): 
    if self.word_counts is None: 
      self.word_counts = {}

      for row in self.raw_data:
        for word in row[0]: 
          self.load_word(word, self.word_counts)

    return dict(self.word_counts)

  def get_ordered_word_counts(self): 
    if self.ordered_counts is None: 
      d = self.get_word_counts()
      pairs = sorted(d.items(), key = lambda x:x[1], reverse=True)
      self.ordered_counts = OrderedDict() 

      for pair in pairs: 
        self.ordered_counts[pair[0]] = pair[1] 

    return OrderedDict(self.ordered_counts)

  def get_most_occurring(self, n): 
    return self.ordered_counts().keys()[:n]
  
  def word_counts(self, l, ws): 
    d = {} 
    for word in l: 
      self.load_word(word, d)
    return [ d[w] if w in d else 0 for w in d.iterkeys() ] 
