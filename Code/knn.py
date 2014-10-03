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

    def predict(k, dataset, labels, testset):
        """
        Given a dataset and corresponding dataset labels
        and a test set
        Apply k nearest neighbors method
        Return a list of lables as predications for each instance in the test set.
        """

        # initilize a list of prediction labels to return
        labels_toreturn = []

        # for each instance in the test set
        # calculate distance between the test instance and every instance in the dataset
        for i in range(len(testset)):    # Loop over each test instance
            # initialize the distance list
            distances = []  
            for j in range(len(dataset)):   # Loop over each instance in the dataset
                # calculate distances based on a given metric
                # add the distance and the index j into the list
                distances.append(metric(i,j), j)

            # k nearest neighbors
            k_neighbors = sorted(distances)[:k]

            # get corresponding labels for these k nearest neighbors
            k_labels = []
            for dist, idx in k_neighbors:
                # retrieve label class and store into dlabel
                k_labels.append(labels[idx])
            # select the majority of labels as a prediction for i
            label_i = np.argmax(np.bincount(k_labels))
            # add this label to a return list
            labels_toreturn.append(label_i);
            
        # return predicated lables for the test set
        return labels_toreturn

    # need to find a reasonable way to calculate distance between two bags of words....
    def metric(i, j):
        """
        Given two instances i and j (without labels)
        return the distance between them
        """
        return 1
   


 