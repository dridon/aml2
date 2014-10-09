import numpy as np
import csv

class SampleCounter: 
  def __init__(self, words, categories, labelled = True, buff = 97000, booleans = False):
    self.words = words 
    self.indices = { self.words[i] : i for i in range(len(self.words)) } 

    self.categories = categories
    self.labelled = labelled

    tp = np.int16 if not booleans else np.int8 

    self.process_list = np.zeros((buff, len(self.words)), dtype=tp) 
    self.labels = np.zeros(buff, np.int8)
    self.buff_index = 0 
    self.booleans = booleans

  def next_buff_index(self): 
    index = self.buff_index
    self.buff_index = self.buff_index + 1
    return index

  def process_sample(self, item):
    index = self.next_buff_index()
    l = self.process_list[index]
    l.fill(0)
    sample = None

    if self.labelled: 
      self.labels[index] = self.categories[item[1]]
      sample = item[0] 
    else: 
      sample = item

    for w in sample: 
      if w in self.indices: 
        i = self.indices[w] 

        if self.booleans: 
          l[i] = 1  
        else: 
          l[i] = l[i] + 1

  def write(self, fname): 
    self.writer = csv.writer(open(fname, "w+"))
    header = self.words + ["category"] if labelled else self.words
    self.writer.writerow(header)
    self.writer.writerows(self.process_list)
