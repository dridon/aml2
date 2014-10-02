""" 
 Combines the two csvs in to a single csv
""""

input_file_name = "../../Datasets/train_input.csv"
output_file_name = "../../Datasets/train_output.csv"

inputs = read_csv(input_file_name) 
outputs = read_csv(output_file_name) 

merged = merge_list(inputs, outputs, 0, 0)
save_csv(merged, "../../Datasets/processed/merged.csv")
