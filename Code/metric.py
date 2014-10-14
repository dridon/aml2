import scipy.spatial.distance as dist
import numpy as np

################################# Auxliary Metric functions #################################

# This metric returns the sum of absolute value of difference between each element in the array
def metric_manhattan(i, j):
    """
    Given two array i and j representing test input and train input respectively
    (where i and j has same number of elements)
    return the manhattan distance between them
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

def metric_manhattan_2(i, j):
    return dist.cityblock(i,j) 


def metric_euclidean(i, j):
    """
    Given two array i and j representing test input and train input respectively
    (where i and j has same number of elements)
    return the euclidean distance between them
    """
    # initialize the distance between i and j
    distance = 0
    # Loop over each number    
    for ii in i: 
        # Loop over each number except the last one  
        for jj in j:   
            # calculate distance based on a given metric
            distance = distance + (ii-jj)**2
    # return the distance between i and j        
    return np.sqrt(distance)

def metric_euclidean_2(i, j):
    return dist.euclidean(i,j) 

def metric_cosine(i,j):
     """
    Given two array i and j representing test input and train input respectively
    (where i and j has same number of elements)
    return the cosine distance between them
    """
    return 1 - np.dot(i,j)/(np.linalg.norm(i)*np.linalg.norm(j))

def metric_cosine_2(i, j):
    return dist.cosine(i, j) 

def metric_braycurtis(i,j):
    """
    Given two array i and j representing test input and train input respectively
    (where i and j has same number of elements)
    return the braycurtis distance between them
    """
    numerator = 0
    denominator = 0
    # Loop over each number    
    for ii in i: 
        # Loop over each number except the last one  
        for jj in j:   
            # calculate distance based on a given metric
            numerator = numerator + abs(ii-jj)
            denominator = denominator + abs(ii+jj)
    # return the distance between i and j        
    return (numerator/denominator)

def metric_braycurtis_2(i, j):
    return dist.braycurtis(i, j)  