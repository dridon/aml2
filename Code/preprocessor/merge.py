import csv
from collections import OrderedDict

def read_csv(file_name, d=",", ignore_header=True):
  """
    Reads a csv in to a 2D list, takes a file name and a delimiter
  """
  f = open(file_name, "r")
  rows = csv.reader(f, delimiter = d)
  return  [ r for r in rows ] 

def list2dict(l, key_col): 
  """ 
    Takes a list and converts it to a dictionary using the specified column, 
    the column is not included in the values and the entries must be unique
  """
  d = OrderedDict()
  for row in l: 
    d[row[key_col]] = row[:key_col] + row[key_col+1:]
  return d

def same_keys(d1, d2):
  """ 
    Returns true if d1 and d2 have the same set of keys 
  """ 
  return set(d1.keys()) == set(d2.keys())

def merge_list(l1, l2, col1, col2): 
  """
    Merges two lists based on the column values
  """
  d1 = list2dict(l1, col1)
  d2 = list2dict(l2, col2)

  mergable = same_keys(d1, d2)
  l = [] 

  if mergable: 
    l = [ d1[k] + d2[k] for k in d1.keys() ]
  else: 
    print "[Warning] Unequivalent Keysets: Merge column does not have same set" 

    l = [ d1[k] + d2[k] for k in d1.keys() if k in d2 ]  
  return l 

def save_csv(l, file_name, d=","):
  """
    Writes a 2D List to a csv file
    Takes a list, file name [and delimiter] 
  """
  f = open(file_name, "w+")
  w = csv.writer(f, delimiter=d)
  w.writerows(l)
