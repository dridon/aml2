import sample_counter as sc
import csv
from sklearn.feature_selection import VarianceThreshold
from numpy import genfromtxt, newaxis
import numpy as np
from sklearn.metrics import confusion_matrix
# from classifiers import *
from sklearn.cross_validation import StratifiedKFold
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from math import log
from sklearn import svm

# samples = scounter.process_list
# selector = VarianceThreshold()
# selector.fit(samples)
# indices = selector.get_support()

# print "Writing to file..."
# scounter.write()

class RandomForest():
    
    def __init__(self, n_trees=100, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, 
                 max_features='auto', max_leaf_nodes=None, bootstrap=True, oob_score=False, n_jobs=-1, random_state=None,
                 verbose=0, min_density=None, compute_importances=None): 
        """
        The random forest has a LOT of parameters. This will be fun to cross-validate.
        I think scikit learn has a cross-validate function.
        """       
        self.random_forest = RandomForestClassifier(n_trees, criterion, max_depth, min_samples_split, min_samples_leaf, 
                 max_features, max_leaf_nodes, bootstrap, oob_score, n_jobs, random_state,
                 verbose, min_density, compute_importances)
        
    def train(self, dataset):
        """
        Train the Random Forest classifier.
        Takes a dataset of ints with one sample per row,
        with the sample's label at the last column.
        """    
        self.random_forest.fit(dataset[:,:-1], dataset[:,-1])
        
    def test(self, dataset):
        """
        Test the Random Forest classifier.
        Takes a dataset of ints with one sample per row,
        with the sample's label at the last column.
        Return the array of predicted classes for each sample
        and the prediction accuracy. 
        """  
        predictions = np.zeros(len(dataset), int)
        
        accuracy = self.random_forest.score(dataset[:,:-1], dataset[:,-1]) # Predict and compute accuracy.
        predictions = self.predict(dataset[:,:-1]) # Predict and return list of predictions.
        
        return predictions, accuracy
        
    def predict(self, samples):
        """
        Predict using the Random Forest classifier.
        Takes a test set of ints with one sample per row.
        Return the array of predicted classes for each sample.
        """  
        return self.random_forest.predict(samples)

def load_dataset(file_name, var_type):
    """
    Load a csv file and converts it to
    a 2D numpy array. Assumes each line is a sample
    and the last column contains the labels.
    Takes a csv filename and the variable type.
    """
    if type(file_name) == str:
        # open the file
        f = open(file_name, 'r')
    else:
        # then file_name is an iterable object
        f = file_name        
    
    dataset = genfromtxt(f, var_type, delimiter=',')
    
    return dataset
    
def get_confusion_matrix(Y1, Y2):    
    """
    Generate the confusion matrix between
    the expected outputs and the classifier outputs.    
    Y1: 1D array of expected outputs.
    Y2: 1D array of classifier outputs.
    """    
    # Compute confusion matrix
    matrix = confusion_matrix(Y1, Y2)
    
    print(matrix)
    
    # Show confusion matrix in a separate window.
    plt.matshow(matrix)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    
def get_k_fold_partition(samples, labels, k = 5):
    """
    Divides a dataset into a training set
    and a validation set. 
    The folds are made by preserving the percentage of samples for each class.
    Takes the dataset and k as parameters.
    Return the train set and the test set.
    """   
    if k < 2:  # k must be at least 2
        k = 2
        
    # samples = dataset[:,:-1]    
    # labels = dataset[:,-1]  
    folds = StratifiedKFold(labels, k) # Generate the fold indexes.
    
    # Build the 2 sets:
    for train_index, test_index in folds:
        X_train, X_test = samples[train_index], samples[test_index]
        y_train, y_test = labels[train_index], labels[test_index]
        
    train_set = np.concatenate((X_train, y_train[:,newaxis]), axis = 1)
    test_set = np.concatenate((X_test, y_test[:,newaxis]), axis = 1)
            
    return train_set, test_set
    
fdf = "../../Datasets/processed/filtered_words_stemmed.csv"
awf = "../../Datasets/processed/all_words_stemmed.csv"
ctf = "../../Datasets/processed/categories_stemmed.csv"
labelled = True

output_file = "/tmp/faiz/aml2/sample_counts_stemmed_1k.csv"

fdr = csv.reader(open(fdf, "r"))
awr = csv.reader(open(awf, "r"))
ctr = csv.reader(open(ctf, "r"))

words = [ w[0] for w in awr ] 
words = words [:15000]
categories = { r[0] : r[1] for r in ctr }

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
  if i % 1000 == 0: print "\tcompleted " + str(i) + " samples"

dataset = scounter.process_list
selector = VarianceThreshold(threshold=0.001)

samples = scounter.process_list
labels = scounter.labels

samples_reduced = selector.fit_transform(samples)
print len(samples_reduced[0])
training_set, validation_set = get_k_fold_partition(samples_reduced, labels, 5)

print " "
print "Training the SVM classifier..."     

s = svm.SVC(kernel='rbf')
s.fit(samples, labels)
print "Testing the SVM classifier..." 
predictions, accuracy = s.test(validation_set)
print "SVM accuracy: ", accuracy 
print "SVM confusion matrix:"
get_confusion_matrix(validation_set[:,-1], predictions)
