import preprocessor.sample_counter as sc
import csv
from collections import OrderedDict

def get_features(stemming = False, test=False, inbool = False, fsuffix="", limit = None):
  # input file name 
  ctf= "../Datasets/processed/categories"
  fdf= "../Datasets/processed/filtered_words"
  awf = "../Datasets/processed/2k_best_words"
  output_file = ""
  ssuff = "" 
  ssuff = ssuff + "_stemmed" if stemming else ssuff
  ssuff = ssuff + fsuffix
  tsuff = ssuff + "_test.csv"
  ssuff = ssuff + "_train.csv"

  fdr = csv.reader(open(fdf + ssuff if not test else fdf + tsuff, "r"))
  awr = csv.reader(open(awf + ssuff, "r"))
  ctr = csv.reader(open(ctf + ssuff, "r"))

  print "Loading word dictionary..."
  words = [w[0] for w in awr]

  print "Loading categories..."
  categories = { r[0] : r[1] for r in ctr }

  filtered_words = [] 
  scounter = None  

  print "Loading data..."
  if not test: 
    for item in fdr: 
      filtered_words.append((item[:-1], item[-1]))
    buff = limit if limit is not None else len(filtered_words)
    scounter = sc.SampleCounter(words, categories, booleans=inbool, buff=buff)
  else: 
    for item in fdr: 
      filtered_words.append(item)
    buff = limit if limit is not None else len(filtered_Words)
    scounter = sc.SampleCounter(words, categories, labelled=False, booleans=inbool, buff=buff)

  i = 1
  print "Processing data..."
  for r in filtered_words: 
    scounter.process_sample(r)
    if i % 1000 == 0 : print "\t completed " + str(i) + " samples" 
    i = i  + 1 
    if limit is not None: 
      if i - 1 == limit: break 

  return (scounter.process_list, scounter.labels)
