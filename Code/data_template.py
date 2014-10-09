import preprocessor.sample_counter as sc
import csv
from collections import OrderedDict

def get_data(stemming = False, test=False, inbool = False, fsuffix=""):
  # input file name 
  ctf= "../Datasets/processed/categories"
  fdf= "../Datasets/processed/filtered_words"
  awf= "../Datasets/processed/word_count_dictionary"
  output_file = ""
  ssuff = "" 
  ssuff = ssuff + "_stemmed" if stemming else ssuff
  ssuff = ssuff + fsuffix
  ssuff = ssuff + "_test" if test else ssuff + "_train"
  ssuff = ssuff + ".csv"

  fdr = csv.reader(open(fdf + ssuff, "r"))
  awr = csv.reader(open(awf + ssuff, "r"))
  ctr = csv.reader(open(ctf + ssuff, "r"))


  wd = OrderedDict() 
  for r in awr: 
    if int(r[1]) > 5: 
      wd[r[0]] = int(r[1])

  words = wd.keys()
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

  i = 0
  for r in filtered_words: 
    scounter.process_sample(r)
    if i % 1000 == 0 : print "\t completed " + str(i) + " samples" 
    i = i  + 1 
  return (scounter.process_list, scounter.labels, wd.keys())

x = get_data(stemming = False, test = False, inbool = False, fsuffix="")
