import preprocessor.sample_counter as sc
import csv
from collections import OrderedDict
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

def get_data(stemming = False, fsuffix=""):
  # input file name 
  ctf= "../Datasets/processed/categories"
  fdf= "../Datasets/processed/filtered_words"
  awf= "../Datasets/processed/word_count_dictionary"
  output_file = ""
  ssuff = "" 
  ssuff = ssuff + "_stemmed" if stemming else ssuff
  ssuff = ssuff + fsuffix
  ssuff = ssuff + "_train"
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

  for item in fdr: 
    filtered_words.append((item[:-1], item[-1]))
  scounter = sc.SampleCounter(words, categories, booleans=False)

  i = 0
  for r in filtered_words: 
    scounter.process_sample(r)
    if i % 1000 == 0 : print "\t completed " + str(i) + " samples" 
    i = i  + 1 
  return (scounter.process_list, scounter.labels, words)

features, labels, words  = get_data(stemming = False, fsuffix="")

kbest = SelectKBest(chi2, k = 2000).fit(features, labels)
indices = kbest.get_support(indices = True)

words_new = [] 
for i in indices: 
  words_new.append([words[i]])

writ = csv.writer(open("../Datasets/processed/2k_best_words_train.csv", "w+"))
writ.writerows(words_new)
