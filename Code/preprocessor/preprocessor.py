import word_counts as wc
from pygments.token import Token 
import lexers as lx
from collections import OrderedDict

class PreProcessor(): 
  categories = OrderedDict() 
  category_count = 0 
  filters = None 
  transforms = None
  processed = None
  processed_booleans = None
  dictionary = None
  ft_data = None
  top_words = None
  
  def __init__(self, unprocessed_data, accept_filters = None, reject_filters = None, transforms = None, top_word_count = 100, stem=False, labelled = True, categories = None): 
    if accept_filters is not None: 
      self.accept_filters = accept_filters 

    if reject_filters is not None: 
      self.reject_filters = reject_filters 

    if transforms is not None:
      self.transforms = transforms

    self.unprocessed_data = list(unprocessed_data)
    self.tokenized_data, ls = lx.tokenize_list(unprocessed_data, verbose=True, stem=stem, labelled = labelled)
    self.top_word_count = top_word_count
    self.labelled = labelled

    """
      This value is hard coded to keep things consistent during runs, it should 
      be removed in the final version
    """
    if categories is None: 
      self.categories['cs'] = 0
      self.categories['stat'] = 1
      self.categories['physics'] = 2 
      self.categories['math'] = 3 
    else: 
      for k,v in categories.items(): 
        self.categories[k] = v

    if labelled: self.labels = [k for k in ls]
    self.process_data()

  def get_categories(self): 
    """
      Gets the mappings of categories to their numerical values.
      It returns an empty dictionary if sample data is not processed.
    """
    return self.categories

  def passes_filters(self, t): 
    """
      Returns true if one of the filters is true. Input must be a tokenized
      tuple
    """
    # if any of the accepted filters passed or if no accepted filters passed then true
    accepted = True
    if self.accept_filters is not None:  
      accepted = any([f(t) for f in self.accept_filters]) 

    # if even one rjects 
    rejected = False 
    if self.reject_filters is not None: 
      rejected = any([f(t) for f in self.reject_filters]) 

    return accepted and not rejected

  def transform(self, w): 
    """
      Returns true if one of the filters is true. Input must be a string
    """
    if self.transforms is None: return w
    return reduce(lambda x, v: v(x), self.transforms, w)

  def filter_and_transform_token(self, t): 
    """
      Returns the transformed value of a tokens word if it passes one filter, 
      None otherwise
    """
    fs = self.filters 
    ts = self.transforms
    w = t[1]
    return self.transform(w) if self.passes_filters(t) else None

  def filter_and_transform_list(self): 
    """
      applies given filters and transformations to the data
    """
    td = self.tokenized_data
    ft = []
    i = 1 
    for row in td: 
      l = []
      for token in row:
          w = self.filter_and_transform_token(token)
          if w is not None:
            l.append(w)
      ft.append(l)
      if i % 1000 == 0: print "\tcompleted " + str(i) + " samples" 
      i = i + 1
    return ft

  def process_data(self, force = False): 
    """
      Processes input data according to filters and transforms that are available
    """
    if self.processed is not None and not force: return self.processed
    print "processing data..."
    # first filter and transform the the abstracts to words we want
    print "filtering data..."
    self.ft_data = self.filter_and_transform_list()

    if self.labelled: 
      print "generating word counts..."
      # # helper that eases processing of data
      self.counter = wc.WordCounter(self.ft_data)

      print "creating word dictionary..."
      # # get the word count dictionary 
      self.dictionary = self.word_dict()

      print "getting most occurring words..."
      # # get the most commonly occurring words
      self.top_words = self.most_occurring_words()

  def word_dict(self):
    """
      Returns the dictionary of word counts if data has been filtered and 
      transformed otherwise None
    """
    if self.counter is None: return None
    return self.counter.get_ordered_word_counts()

  def most_occurring_words(self, n = None): 
    """
      Returns the most occurring words if data has been filtered and 
      transformed otherwise None
    """
    n = n if n is not None else self.top_word_count
    if self.counter is None: return None
    n = n if self.top_word_count != -1 else self.counter.max_words()

    return self.counter.most_occurring(self.top_word_count)
