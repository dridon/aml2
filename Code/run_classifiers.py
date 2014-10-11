# -*- coding: utf-8 -*-

from numpy import genfromtxt, newaxis
import numpy as np
from sklearn.metrics import confusion_matrix
from classifiers import *
from knn import * #added by sherry
from sklearn.cross_validation import StratifiedKFold
import matplotlib.pyplot as plt
import feature_generation as ftg

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
        
    folds = StratifiedKFold(labels, k) # Generate the fold indexes.
    
    # Build the 2 sets:
    for train_index, test_index in folds:
        X_train, X_test = samples[train_index], samples[test_index]
        y_train, y_test = labels[train_index], labels[test_index]
        
    train_set = np.concatenate((X_train, y_train[:,newaxis]), axis = 1)
    test_set = np.concatenate((X_test, y_test[:,newaxis]), axis = 1)
            
    return train_set, test_set
    
if __name__ == "__main__":    


    samples, labels = ftg.get_features(stemming=False, test=False, inbool=False, limit = 5000)

   

    
    # Testing    
    training_set, validation_set = get_k_fold_partition(samples, labels, 5)

    #print training_set
    #print validation_set    
         
    # print " "            
    
    # print "Training the Multinomial NB classifier..."   
    # nbm = NaiveBayesMultinomial() 
    # nbm.train(training_set)       
    # print "Testing the Multinomial NB classifier..."  
    # errors, predictions, accuracy = nbm.test(validation_set)
    # print "NB accuracy: ", accuracy 
    # print "NB confusion matrix:" 
    # get_confusion_matrix(validation_set[:,-1], predictions)
     
    # print " "
     
    # print "Training the RF classifier..."     
    # f = RandomForest()
    # f.train(training_set)
    # print "Testing the RF classifier..." 
    # predictions, accuracy = f.test(validation_set)
    # print "RF accuracy: ", accuracy 
    # print "RF confusion matrix:"
    # get_confusion_matrix(validation_set[:,-1], predictions)


    ####################### added by sherry #######################

    print " "            
    

    #print "Training the KNN classifier..."   
    knn = KNearestNeighbor(100) 

    #nbm.train(training_set)       
    print "Testing the KNN classifier..."  
    predictions, accuracy = knn.test(training_set,validation_set)
    print "KNN accuracy: ", accuracy 
    print "KNN confusion matrix:" 
    get_confusion_matrix(validation_set[:,-1], predictions)
    
    
