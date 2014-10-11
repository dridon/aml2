################################# Auxliary Metric functions #################################

# This metric returns the sum of absolute value of difference between each element in the array
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