import sample_counter as sc
import csv

fdf = "../../Datasets/processed/filtered_words_stemmed.csv"
awf = "../../Datasets/processed/all_words_stemmed.csv"
ctf = "../../Datasets/processed/categories_stemmed.csv"
labelled = True

output_file = "/tmp/faiz/aml2/sample_counts_stemmed.csv"

fdr = csv.reader(open(fdf, "r"))
awr = csv.reader(open(awf, "r"))
ctr = csv.reader(open(ctf, "r"))

words = [ w[0] for w in awr ] 
categories = { r[0] : r[1] for r in ctr}
filtered_words = [] 
scounter = None  

if labelled: 
  for item in fdr: 
    filtered_words.append((item[1:], item[0]))

  scounter = sc.SampleCounter(words, categories, output_file)
else: 
  for item in fdr: 
    filtered_words.append(item)
  scounter = sc.SampleCounter(words, categories, output_file, labelled=False)

i = 0 
print "Processing Samples..." 
for sample in filtered_words: 
  scounter.process_sample(sample)
  i = i + 1 
  if i % 100 == 0: print "\tcompleted " + str(i) + " samples"

print "Writing to file..."
scounter.write()
