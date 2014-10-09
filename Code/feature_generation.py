import preprocessor.sample_counter as sc
import csv
from collections import OrderedDict

def get_features(stemming = False, test=False, inbool = False, fsuffix=""):
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

  words = [w[0] for w in awr]
  categories = { r[0] : r[1] for r in ctr }

  filtered_words = [] 
  scounter = None  

  if not test: 
    for item in fdr: 
      filtered_words.append((item[:-1], item[-1]))
    scounter = sc.SampleCounter(words, categories, booleans=inbool)
  else: 
    for item in fdr: 
      filtered_words.append(item)
    scounter = sc.SampleCounter(words, categories, labelled=False, booleans=inbool)

  i = 1
  for r in filtered_words: 
    scounter.process_sample(r)
    if i % 1000 == 0 : print "\t completed " + str(i) + " samples" 
    i = i  + 1 
  return (scounter.process_list, scounter.labels)