# -*- coding: utf-8 -*-
import numpy as np
from sklearn.ensemble import RandomForestClassifier

#My implementation is not efficient! Might need to optimize when we use the real dataset.
class NaiveBayes:
    
    def train(self, dataset, alpha = 1):
        """
        Train the Naive Bayes classifier.
        Takes a dataset of ints with one sample per row,
        with the sample's label at the last column. 
        The classes must be 0 indexed.
        Alpha is used for Laplace smoothing. We could cross-validate over this guy.
        """    
        dataset = dataset[dataset[:,-1].argsort()] # Sort the dataset by classes.
        #print dataset
        
        ########
        # Compute p(y=1) for all ys.
        ########
        label_counts = np.bincount(dataset[:,-1]) # Get the number of occurrences of each class, sorted.  
        self.p_ys = label_counts * 1.0 / len(dataset) # Compute probs. 
       
        ########
        # Compute p(x|y) for all x,y.
        ########
        self.feature_count = len(dataset[0]) - 1 
        self.class_count = len(label_counts)
        
        self.p_xi_given_ys = np.zeros((self.class_count, self.feature_count))   # Initialize matrix
        start_index = 0
        for i in range(self.class_count):  # Loop over each class          
            end_index = start_index + label_counts[i] # end of this class index   
            class_word_counts = np.sum(dataset[start_index:end_index,:-1]) # sum all words of class i    
            denominator = class_word_counts + alpha * self.feature_count # Here we add the feature_count as Laplace smoothing
            
            for j in range(self.feature_count):  # Loop over each feature
                single_word_count = np.sum(dataset[start_index:end_index,j]) # sum number times word j appears in class i   
                numerator = single_word_count + alpha
                self.p_xi_given_ys[i][j] = numerator * 1.0 / denominator    # Compute p(xi|y)
            
            start_index = end_index
            
    def test(self, samples):
        """
        Compute P(y|x) for each class, 
        and select the class with highest probability. 
        Return the array of prediction errors (0:good/1:error)
        and the prediction accuracy."""
        prediction_errors = np.zeros(len(samples), int)
        class_predictions = np.zeros(self.class_count)
                
        for i in range(len(samples)):    # Loop over each sample
            for j in range(self.class_count):   # Loop over each class
                class_predictions[j] = self.p_ys[j]   # Get p(y) for class j
                for k in range(self.feature_count): # Loop over each feature
                
                    # Multiply p(y) by p(xi|y) if the sample entry is non-zero 
                    if(samples[i][k] != 0):
                        class_predictions[j] *= self.p_xi_given_ys[j][k]
                    # Else multiply by 1 - p(xi|y)
                    else: 
                        class_predictions[j] *= 1 - self.p_xi_given_ys[j][k]
                
            predicted_class = np.argmax(class_predictions)  # Prediction is class with highest probability.
            
            # Check if the predicted class doesn't match the true class.
            if(predicted_class != samples[i][-1]):
                prediction_errors[i] = 1     
                
        # Compute accuracy
        accuracy = 1 - (np.sum(prediction_errors) * 1.0 / len(prediction_errors))      
            
        return prediction_errors, accuracy    
    
    def predict(self, samples):
        """
        Compute P(y|x) for each class, 
        and select the class with highest probability. 
        Return the array of class predictions."""
        predictions = np.zeros(len(samples), int)
        class_predictions = np.zeros(self.class_count)
        
        for i in range(len(samples)):    # Loop over each sample
            for j in range(self.class_count):   # Loop over each class
                class_predictions[j] = self.p_ys[j]   # Get p(y) for class j
                for k in range(self.feature_count): # Loop over each feature
                
                    # Multiply p(y) by p(xi|y) if the sample entry is non-zero 
                    if(samples[i][k] != 0):
                        class_predictions[j] *= self.p_xi_given_ys[j][k]
                    # Else multiply by 1 - p(xi|y)
                    else: 
                        class_predictions[j] *= 1 - self.p_xi_given_ys[j][k]
                
            predictions[i] = np.argmax(class_predictions)  # Prediction is class with highest probability.
            
        return predictions    
   
# Not finished yet. Working on it.         
class RandomForest():
    def __init__(self):        
        self.random_forest = RandomForestClassifier()#set params here
        
    def train(self, dataset):
        self.random_forest.fit(dataset[:,:-1], dataset[:,-1])
        
    def test(self, dataset):
        return self.random_forest.score(dataset[:,:-1], dataset[:,-1])
        
    def predict(self, samples):
        self.random_forest.predict(samples)

def toy_data():
    """
    Create random dataset for testing purposes.
    Columns 0 to 4 contain the features, and 5 the labels.
    """ 
    #dataset = np.zeros((10,5), np.int)
    dataset = np.array([[0,0,0,0,4],
                       [0,0,0,0,5],
                       [1,3,0,0,0],
                       [3,1,0,0,1],
                       [0,0,6,2,0],
                       [0,0,0,0,0],
                       [0,0,1,7,2],                           
                       [0,0,5,1,5],
                       [0,0,34,0,0],
                       [0,0,3,0,0]])
    Y = np.array([3,3,2,2,1,0,1,1,0,0])
    #for i in range(10):
        #for j in range(5):
            #dataset[i][j] = np.random.randint(0,10)  
    dataset = np.column_stack((dataset, Y))
    return (dataset)       

# Testing
#c = NaiveBayes()
dataset = toy_data()
#c.train(dataset,1)   
#predictions = c.predict(dataset)  
#print predictions
f = RandomForest()
f.train(dataset)
print f.test(dataset)

   
