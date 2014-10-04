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
tfms = [ts.to_lower]

# Number of most occurring words to take for feature counts, -1 for all of them just realize there are between 30,000 and 40,000 words and your machine might hang
n = 1000 

# Toggle this boolean if you want to save to csvs 
save2csv = True 

# This toggles stemming 
stemming = False

# Dictionary output file name and path
categories_csv = "../../Datasets/processed/categories.csv"
dict_csv = "../../Datasets/processed/word_count_dictionary.csv"
sample_counts_csv = "../../Datasets/processed/sample_counts.csv"
sample_booleans_csv = "../../Datasets/processed/sample_booleans.csv"

# files for stemming output
# categories_csv = "../../Datasets/processed/categories_stemmed.csv"
# dict_csv = "../../Datasets/processed/word_count_dictionary_stemmed.csv"
# sample_counts_csv = "../../Datasets/processed/sample_counts_stemmed.csv"
# sample_booleans_csv = "../../Datasets/processed/sample_booleans_stemmed.csv"


"""
Code, you shouldn't really need to touch this unless there's something very
specific required
"""
# Merge the csvs in to one list
input_file_name = "../../Datasets/train_input.csv"
output_file_name = "../../Datasets/train_output.csv"
inputs = merge.read_csv(input_file_name) 
outputs = merge.read_csv(output_file_name) 
merged = merge.merge_list(inputs, outputs, 0, 0)

# create the preprocessor
pp = prp.PreProcessor(merged, accepts, rejects, tfms, n, stem=stemming)

# save to csv if needed
if save2csv: 
  categories = pp.get_categories() 
  worddict = pp.word_dict()
  sample_counts = pp.sample_counts() 
  sample_booleans = pp.sample_booleans()

  cw = csv.writer(open(categories_csv, "w+"))
  ww = csv.writer(open(dict_csv, "w+"))
  scw = csv.writer(open(sample_counts_csv, "w+"))
  sbw = csv.writer(open(sample_booleans_csv, "w+")) 

  cw.writerows(categories.items())
  ww.writerows(worddict.items())
  scw.writerows(sample_counts) 
  sbw.writerows(sample_booleans)
