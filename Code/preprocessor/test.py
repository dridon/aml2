import preprocessor as pp
import word_counts as wc

reload(pp)
reload(lx)

prp = pp.PreProcessor(test, accepts, rejects, tfms)
filtered_vals = prp.filter_and_transform_list() 
prp.process_data()
