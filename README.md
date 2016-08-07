# id3
#Hello everyone! This is my id3 implementation, based on this code https://mariuszprzydatek.com/2014/11/11/iterative-dichotomiser-3-id3-algorithm-decision-trees-machine-learning/

#Algorithm is applied to arrythmia dataset( uci machine learning repository) and the purpose was to establish if a patient will have or not
#cardiac arrythmia.

#I mantain the fundamental idea of implementing the tree through a dictionary of dictionary. I add some code to handle continous attribute.
#The idea, suggested from some posts on the internet, was to apply information gain to decide the value of the continous attribute on which 
#data will be splitted. all this code is contained in id3.py file. 

#Since original data is made of 200 or more attributes, i make two test (chisqtest  for categorial data and point-biserial correlation for continous data) 
#to decide a priori if an attribute will influence classification. this code is in variableselection.py.

#In performancecv.py you will find an implementation of k-fold cross validation and some code to compute performance. 
#since the algorithm is applied with aim of classification, performance is computed in terms of confusion matrix and accuracy.

#there's also a code to print the resulting tree.

#Hope you like it
