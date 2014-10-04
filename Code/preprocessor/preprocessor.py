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
  
  def __init__(self, unprocessed_data, accept_filters = None, reject_filters = None, transforms = None, top_word_count = 100): 
    if accept_filters is not None: 
      self.accept_filters = accept_filters 

    if reject_filters is not None: 
      self.reject_filters = reject_filters 

    if transforms is not None:
      self.transforms = transforms

    self.unprocessed_data = list(unprocessed_data)
    self.tokenized_data = lx.tokenize_list(unprocessed_data, 0, verbose=False)
    self.top_word_count = top_word_count

    self.process_data()

  def next_category_key(self): 
    """
      Generates the next number to be used as a category index 
    """
    index = self.category_count
    self.category_count = self.category_count + 1 
    return index 

  def get_category(self, k): 
    """
      Gets the numberical category for a category k
    """
    if k not in self.categories: 
      self.categories[k] = self.next_category_key()
    return self.categories[k]

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
    for row in td: 
      l = []
      for token in row[0]:
          w = self.filter_and_transform_token(token)
          if w is not None:
            l.append(w)
      ft.append([l, row[1]])
    return ft

  def filter_and_transform(self, accept_filters, reject_filters, transforms): 
    """
      Sets the filters and transforms for the PreProcessor instance and 
      reprocessess the initial data with regards to these filters and 
      transforms
    """
    self.accept_filters = accept_filters 
    self.reject_filters = reject_filters
    self.transforms = transforms 
    self.process_data(force=True)

  def process_data(self, force = False): 
    """
      Processes input data according to filters and transforms that are available
    """

    if self.processed is not None and not force: return self.processed

    # first filter and transform the the abstracts to words we want
    self.ft_data = self.filter_and_transform_list()

    # # helper that eases processing of data
    self.counter = wc.WordCounter(self.ft_data)

    # # get the word count dictionary 
    self.dictionary = self.word_dict()

    # # get the most commonly occurring words
    self.top_words = self.most_occurring_words()

    # # get a list of the counts of the samples
    self.processed = self.sample_counts(force=True)

    # # booleans of processed values
    self.processed_booleans = self.sample_booleans(force=True)

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

    return self.counter.most_occurring(self.top_word_count)

  def sample_counts(self, force = False): 
    """
      Returns the word counts of the top most occurring words over all samples
    """
    if self.ft_data is None or self.top_words is None: return None
    if not force: return self.processed

    samples = [] 
    samples.append(self.top_words + ["category"])
    for row in self.ft_data: 
      sample = row[0]
      samples.append(self.counter.str_word_counts(sample, self.top_words) + [self.get_category(row[1])])
    return samples

  def sample_booleans(self, force=False): 
    """
      Returns a version of the sample counts in boolean format if the count 
      of a word is greater than 0
    """
    if self.processed is None: return None
    if not force: return self.processed_booleans

    samples = iter(self.processed) 
    bool_samples = [next(samples)]
    for row in samples:
      bool_samples.append([ c > 0 for c in row[:-1]] + [row[-1]])
    return bool_samples
