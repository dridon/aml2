"""
Script that takes input and places it in to output
"""
import merge
import lexers as lx
import filters as fs 
import transforms as ts 
import preprocessor as prp 
import csv

"""
Settings, change these to alter script parameters
"""
# These are the filters are token matchers, any token that matches one of these will get through 
accepts = [fs.words]

# These filters are rejections, out of the ones that made it through, if any of them passes a reject test, it is not included
rejects = [fs.lt_three_chars]

# Transforms, these are the transformations you want accepted words to go through
tfms = [ts.to_lower, ts.no_back_slash]

# Number of most occurring words to take for feature counts, -1 for all of them just realize there are between 30,000 and 40,000 words and your machine might hang
n = -1  

# Toggle this boolean if you want to save to csvs 
save2csv = True 

# This toggles stemming 
stemming = True 
 
#suffix to be appended to file names
fsuffix = "_train"

# Dictionary output file name and path
categories_csv = "../../Datasets/processed/categories"
dict_csv = "../../Datasets/processed/word_count_dictionary"
fw_csv = "../../Datasets/processed/filtered_words"
aw_csv = "../../Datasets/processed/all_words"

# Input data, no need to have output file name if test data
input_file_name = "../../Datasets/train_input.csv"
output_file_name = "../../Datasets/train_output.csv"

"""
Code, you shouldn't really need to touch this unless there's something very
specific required
"""
merged =[]
inputs = merge.read_csv(input_file_name) 
outputs = merge.read_csv(output_file_name) 
merged = merge.merge_list(inputs, outputs, 0, 0)

# create the preprocessor
pp = prp.PreProcessor(merged, accepts, rejects, tfms, n, stem=stemming, labelled = True)

# save to csv if needed
if save2csv: 
  categories = pp.get_categories() 
  worddict = pp.word_dict()
  ft_words = pp.ft_data
  allwords = pp.top_words
  labels  = pp.labels

  ssuff = "" 
  ssuff = ssuff + "_stemmed" if stemming else ssuff
  ssuff = ssuff + fsuffix
  ssuff = ssuff + ".csv"

  cw = csv.writer(open(categories_csv + ssuff, "w+"))
  ww = csv.writer(open(dict_csv + ssuff , "w+"))
  fw = csv.writer(open(fw_csv + ssuff, "w+"))
  aw = csv.writer(open(aw_csv + ssuff, "w+"))

  for i in range(len(ft_words)):
    r = ft_words[i] + [labels[i]]
    fw.writerow(r)

  cw.writerows(categories.items())
  ww.writerows(worddict.items())

  for w in allwords: 
    aw.writerow([w])
