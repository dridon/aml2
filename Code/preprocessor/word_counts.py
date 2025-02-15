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
      print "getting word counts..."
      self.word_counts = {}

      i = 1
      for row in self.data:
        if i % 1000 == 0: print "\tcompleted " + str(i) + " samples"
        i = i + 1 
        for word in row: 
          self.load_word(word, self.word_counts)

    return dict(self.word_counts)

  def get_ordered_word_counts(self, force = False): 
    """ 
      Gets the counts of all the words in the data in an OrderedDict in 
      descending order of their counts
    """
    if self.ordered_counts is None and not force: 
      d = self.get_word_counts()

      print "ordering word counts..."
      pairs = sorted(d.items(), key = lambda x: x[1], reverse=True)
      self.ordered_counts = OrderedDict() 

      for k,v in pairs: 
        self.ordered_counts[k] = v 

    return OrderedDict(self.ordered_counts)

  def most_occurring(self, n): 
    """
      Gets the most ocurring the first n most occurring words or all the words
      if n > the number of words
    """
    return self.get_ordered_word_counts().keys()[:n]

  def max_words(self): 
    """
      Gets the count of the words
    """
    words = self.get_word_counts() 
    return len(words.keys())

  def str_word_counts(self, l, kws): 
    """
      For all the words in kws, it gets the counts of those words in l
    """
    for word in l: 
      if word in kws: 
        kws[word] = kws[word] + 1 
