import merge
import lexers as lx

# Merge the csvs in to one list
input_file_name = "../../Datasets/train_input.csv"
output_file_name = "../../Datasets/train_output.csv"
inputs = merge.read_csv(input_file_name) 
outputs = merge.read_csv(output_file_name) 
merged = merge.merge_list(inputs, outputs, 0, 0)

tokenized_list = lx.tokenize_list(merged, 0, verbose=False)
