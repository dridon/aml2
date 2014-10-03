"""
  A helper class to ease preprocessing
"""
from collections import OrderedDict

class WordCounter:
  """ 
    A class that can be used to analyze the counts of a list of samples 
  """

  data = None
  word_counts = None 
  ordered_counts = None

  def __init__(self, data): 
    self.data = data

  def load_word(self, w, d): 
    """ 
      Increments the count of a word w stored in a dictionary d
    """
    if w not in d: 
      d[w] = 0 
    d[w] = d[w] + 1 

  def get_word_counts(self): 
    """ 
      Gets the counts of all the words in the data 
    """
    if self.word_counts is None: 
      self.word_counts = {}

      for row in self.data:
        for word in row[0]: 
          self.load_word(word, self.word_counts)

    return dict(self.word_counts)

  def get_ordered_word_counts(self): 
    """ 
      Gets the counts of all the words in the data in an OrderedDict in 
      descending order of their counts
    """
    if self.ordered_counts is None: 
      d = self.get_word_counts()
      pairs = sorted(d.items(), key = lambda x:x[1], reverse=True)
      self.ordered_counts = OrderedDict() 

      for k,v in pairs: 
        self.ordered_counts[k] = v 

    return OrderedDict(self.ordered_counts)

  def most_occurring(self, n): 
    """
      Gets the most ocurring the first n most occurring words or all the words
      if n > the number of words
    """
    return self.ordered_counts().keys()[:n]

  def max_words(self): 
    """
      Gets the count of the words
    """
    words = self.get_word_counts() 
    return len(words.keys())
  
  def word_counts(self, l, kws): 
    """
      For all the words in kws, it gets the counts of those words in l
    """
    d = {} 
    for word in l: 
      self.load_word(word, d)
    return [ d[w] if w in d else 0 for w in kws ] 