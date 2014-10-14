import feature_generation as ftg
import csv

# samples, labels = ftg.get_features(stemming=False, test=False, inbool=False, limit = None)
# wr = csv.writer(open("../Datasets/final/bag_of_words_training_unstemmed.csv", "w+"))
# print "Writing non stemmed training bag of words..."
# i = 0
# for i in range(len(samples)): 
#   wr.writerow(samples[i] + [labels[i]])
#   i = i + 1
#   if i % 1000 == 0: 
#     print "\tcompleted " + str(i) + " samples" 


samples, labels = ftg.get_features(stemming=True, test=False, inbool=False, limit = None)
wr = csv.writer(open("../Datasets/final/bag_of_words_training_stemmed.csv", "w+"))
print "Writing stemmed training bag of words..."
i = 0
for i in range(len(samples)): 
  wr.writerow(samples[i] + [labels[i]])
  i = i + 1
  if i % 1000 == 0: 
    print "\tcompleted " + str(i) + " samples" 

samples, labels = ftg.get_features(stemming=False, test=False, inbool=True, limit = None)
wr = csv.writer(open("../Datasets/final/booleans_training_unstemmed.csv", "w+"))
print "Writing non stemmed training booleans..."
i = 0
for i in range(len(samples)): 
  wr.writerow(samples[i] + [labels[i]])
  i = i + 1
  if i % 1000 == 0: 
    print "\tcompleted " + str(i) + " samples" 


samples, labels = ftg.get_features(stemming=True, test=False, inbool=True, limit = None)
wr = csv.writer(open("../Datasets/final/booleans_training_stemmed.csv", "w+"))
print "Writing stemmed training booleans..."
i = 0
for i in range(len(samples)): 
  wr.writerow(samples[i] + [labels[i]])
  i = i + 1
  if i % 1000 == 0: 
    print "\tcompleted " + str(i) + " samples" 
