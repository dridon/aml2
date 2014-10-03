from word_counts import WordCounter
from pygments.token import Token 
import lexers as lx

class PreProcessor(): 
  categories = {} 
  category_count = 0 
  filters = None 
  transforms = None
  processed = None
  processed_booleans = None
  dictionary = None
  ft_data = None
  top_words = None
  
  def __init__(self, unprocessed_data, filters = None, transforms = None, top_word_count = 5): 
    if filters is not None: 
      self.filters = filters 

    if transforms is not None:
      self.transforms = transforms

    self.unprocessed_data = list(unprocessed_data)
    self.tokenized_data = lx.tokenize_list(unprocessed_data, verbose=False)
    self.top_word_count = top_word_count

  def next_category_key(self): 
    """
      Generates the next number to be used as a category index 
    """
    self.category_count = self.category_count + 1 
    return self.category_count

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

  def one_true(self, t): 
    """
      Returns true if one of the filters is true. Input must be a tokenized
      tuple
    """
    if self.filters is None: return True 
    return any([f(t) for f in self.filters])

  def transform(self, w): 
    """
      Returns true if one of the filters is true. Input must be a word
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
    return transform(w, ts) if one_true(t, fs) else None

  def filter_and_transform_list(self, l): 
    ft = []
    for row in td: 
      l = []
      for tokens in row[0]:
        for t in tokens:
          w = self.filter_and_transform_token(t)
          if w is not None:
            l.append(w)
      ft.append([l, row[1])
    return ft

  def filter_and_transform(self, fs, ts): 
    """
      Sets the filters and transforms for the PreProcessor instance and 
      reprocessess the initial data with regards to these filters and 
      transforms
    """
    self.filters = fs
    self.transforms = ts
    self.process_data(force=True)

  def process_data(self, force = False): 
    """
      Processes input data according to filters and transforms that are available
    """

    if self.processed is not None and not force: return self.processed

    td = self.tokenized_data

    # first filter and transform the the abstracts to words we want
    self.ft_data = filter_and_transform_list(td)

    # helper that eases processing of data
    self.counter = WordCounter(self.ft_data)

    # get the word count dictionary 
    self.dictionary = self.word_dict()

    # get the most commonly ocurring words
    self.top_words = most_ocurring_words()

    # get a list of the counts of the samples
    self.processed = self.sample_counts(force=True)

    # booleans of processed values
    self.processed_booleans = self.sample_booleans(force=True)

  def word_dict(self):
    """
      Returns the dictionary of word counts if data has been filtered and 
      transformed otherwise None
    """
    if self.counter is None: return None
    return self.counter.get_ordered_word_counts()

  def most_ocurring_words(self): 
    """
      Returns the most occurring words if data has been filtered and 
      transformed otherwise None
    """
    if self.counter is None: return None
    return self.counter.most_ocurring(self.top_word_count)

  def sample_counts(self, force = False): 
    """
      Returns the word counts of the top most occurring words over all samples
    """
    if self.ft_data is None or self.top_words is None: return None
    if not force: return self.processed

    sample = [] 
    samples.append(self.top_words + ["category"])
    for row in self.ft_data: 
      sample = row[0]
      samples.append(self.counter.word_counts(sample, self.top_words) + [self.get_category(row[1])])
    return samples

  def sample_booleans(self, force=False): 
    """
      Returns a version of the sample counts in boolean format if the count 
      of a word is greater than 0
    """
    if self.processed is None: return None
    if not force: return self.processed_booleans

    bool_samples = []
    for row in self.processed:
      bool_samples.append([ c > 0 for c in row[:-1]] + [row[-1]])
    return bool_samples
