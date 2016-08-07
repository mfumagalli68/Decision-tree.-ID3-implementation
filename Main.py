from id3 import *
from performancecv import *
import copy
#nel file variable selection si trova l'applicazione della feature selection. una volta fatta la selection
# è stato scritto un file dove sono state inserite solo le variabili selezionate in modo da non far piu il run
#di variableSelection
data_aritmia=copy.deepcopy(my_data_aritmia_clean[:300])
#prima prova dell'albero sul dataset selezionato, 70% di training, 30% di test
t = int(0.7* len(my_data_aritmia_clean[:300]))
trainingset = my_data_aritmia_clean[0:t]
testset = my_data_aritmia_clean[t:len(my_data_aritmia_clean[:300])]
tree_train = tree(trainingset,col_of_dataset(trainingset,(len(trainingset[0])-1)))
performance_algorithm=performance(trainingset,testset,conf_matrix="no")
print(performance_algorithm)
#applico cv

#data_aritmia_2=copy.deepcopy(data_aritmia)
cv=CV(data_aritmia,matrix="no")
print(cv)

confusion_matrix=CV(data_aritmia,matrix="yes")
print(confusion_matrix)
#calcolo sensitività e specificità
sensitivity=[]
specificity=[]
for i in range(0,len(confusion_matrix)):

    sensitivity.append(confusion_matrix[i]["truePositive"]/(confusion_matrix[i]["truePositive"]+confusion_matrix[i]["falseNegative"]))
    specificity.append(confusion_matrix[i]["trueNegative"] / (confusion_matrix[i]["falsePositive"] + confusion_matrix[i]["trueNegative"]))

print(sensitivity,specificity)