import numpy as np
from metric import *

# Notes:
# 1. should we separate dataset (word counts) from labels?
# 2. how to calculate metric?
 
class KNearestNeighbor:

    def __init__(self, k):
        """       
        k for number of nearest neighbor
        """  
        self.k = k


    def test(self, trainset, testset):
        """
        Given a trainset which has both input and output (output is the last number acted as labels)
        and a test set which also has both input and output (output is the last number acted as labels)
        Apply k nearest neighbors method
        Return a list of lables as predications for each input in the test set,
        as well as the accuracy rate
        """

        # initialize a list of prediction labels for test set to return
        labels_to_return = []

        # initialize a list as prediction errors for test set
        prediction_errors = np.zeros(len(testset), int)

        # for each input in the test set
        # calculate distance between the test input and every input in the trainset

        # Loop over each test input
        for index_i, example_i in enumerate(testset):
            print "Finding k nearest neighbors for test input", index_i
            # discard the label (last element)
            input_i = example_i[:-1]  
            #print input_i
            # initialize the distance list for input i
            distances_i = []  
            # Loop over each example in the dataset
            for index_j, example_j in enumerate(trainset):   
                # discard the label (last element)
                #print "Calculating distance to example ", index_j
                input_j = example_j[:-1]
                # calculate distances based on a given metric
                # add the distance between input_i and input_j, as well as the index j into the list
                distances_i.append((metric_cosine(input_i,input_j), index_j))

            # get k nearest neighbors for input i
            k_neighbors_for_i = sorted(distances_i)[:self.k]
            #print "K nearest neighbors:", k_neighbors_for_i

            # get corresponding labels for these k nearest neighbors
            k_labels_for_i = []
            for dist, idx in k_neighbors_for_i:
                # retrieve label classes and store them
                k_labels_for_i.append(trainset[idx][-1])
            # select the majority of labels as a prediction for test input i
            label_for_i = np.argmax(np.bincount(k_labels_for_i))
            #print "Test input", index_i, "has cateogry: ", label_for_i
            # add this label to a return list
            labels_to_return.append(label_for_i);


            # Check if the predicted label matches the actual label.
            if(labels_to_return[index_i] != testset[index_i][-1]):
                prediction_errors[index_i] = 1     
                
        # Compute accuracy
        accuracy = 1.0 - (np.sum(prediction_errors) * 1.0 / len(prediction_errors))    

            
        # return predicated lables for the test set as well as the accuracy
        return labels_to_return, accuracy
        


    def predict(self, trainset, testset):
        """
        Given a trainset which has both input and output (output is the last number acted as labels)
        (In KNN, we have to remember trainset so that we can select k nearest neighbors from trainset later)
        and a test set which only has input
        Apply k nearest neighbors method
        Return a list of lables as predications for each input in the test set.
        """

        # initilize a list of prediction labels for test set to return
        labels_to_return = []

        # for each input in the test set
        # calculate distance between the test input and every input in the trainset

        # Loop over each test input
        for input_i in testset:    
            # initialize the distance list for input i
            distances_i = []  
            # Loop over each example in the dataset
            for index_j, example_j in enumerate(trainset):   
                # discard the label (last element)
                input_j = example_j[:-1]
                # calculate distances based on a given metric
                # add the distance between input_i and input_j, as well as the index j into the list
                distances_i.append((metric_cosine(input_i,input_j), index_j))

            # get k nearest neighbors for input i
            k_neighbors_for_i = sorted(distances_i)[:self.k]

            # get corresponding labels for these k nearest neighbors
            k_labels_for_i = []
            for dist, idx in k_neighbors_for_i:
                # retrieve label classes and store them
                k_labels_for_i.append(trainset[idx][-1])
            # select the majority of labels as a prediction for test input i
            label_for_i = np.argmax(np.bincount(k_labels_for_i))
            # add this label to a return list
            labels_to_return.append(label_for_i);
            
        # return predicated lables for the test set
        return labels_to_return




   


 