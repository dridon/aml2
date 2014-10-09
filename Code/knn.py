import numpy as np

# Notes:
# 1. should we separate dataset (word counts) from labels?
# 2. how to calculate metric?
 
class KNearestNeighbor:

    def __init__(self, k):
        """       
        k for number of nearest neighbor
        """  
        self.k = k

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
                distances_i.append(metric_abs(input_i,input_j), index_j)

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

    # need to find a reasonable way to calculate distance between two bags of words....
    def metric_abs(i, j):
        """
        Given two array i and j representing test input and train input respectively
        (where i and j has same number of elements)
        return the distance between them
        """
        # initialize the distance between i and j
        distance = 0
        # Loop over each number    
        for ii in i: 
            # Loop over each number except the last one  
            for jj in j:   
                # calculate distance based on a given metric
                distance = distance + abs(ii-jj)
        # return the distance between i and j        
        return distance


 