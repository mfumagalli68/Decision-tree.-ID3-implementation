from id3 import *


# my_data_aritmia_clean=[line for line in my_data_aritmia_clean_quasi if len(line)==94]
# t = int(0.7* len(my_data_aritmia_clean[:350]))
# trainingset = my_data_aritmia_clean[0:t]
# testset = my_data_aritmia_clean[t:len(my_data_aritmia_clean[:350])]
# tree_train = tree(trainingset,col_of_dataset(trainingset,(len(trainingset[0])-1)))
# list_prediction=[]
# for i in range(0,len(testset)):
#     list_prediction.append(classifying(tree_train,testset[i]))

def matches(list1,list2):
    count=0
    a=[i for i in range(0,len(list1)) if list1[i]==list2[i]]
    return len(a)

def performance(trainingset,testset,conf_matrix="no"):
    tree_train = tree(trainingset,col_of_dataset(trainingset,(len(trainingset[0])-1)))
    list_prediction=[]
    true_value=[]
    for i in range(0, len(testset)):
        list_prediction.append(classifying(tree_train, testset[i]))
    for i in range(0,len(testset)):
        true_value.append(testset[i][len(testset[i])-1])

    if(conf_matrix=="yes"):
        dict = {}
        count = 0
        count2 = 0
        count3 = 0
        count4 = 0
        dict["truePositive"]=0
        dict["trueNegative"]=0
        dict["falsePositive"]=0
        dict["falseNegative"]=0

        for j in range(0, len(list_prediction)):
            if (list_prediction[j] == true_value[j] and true_value[j] == 1):
                count = count + 1
                dict["truePositive"] = count
            if (list_prediction[j] == true_value[j] and true_value[j] == 0):
                count2 = count2 + 1
                dict["trueNegative"] = count2
            if (list_prediction[j] == 1 and true_value[j] == 0):
                count3 = count3 + 1
                dict["falsePositive"] = count3
            if (list_prediction[j] == 0 and true_value[j] == 1):
                count4 = count4 + 1
                dict["falseNegative"] = count4
        return dict

    match=matches(true_value,list_prediction)
    right_label_class=match/len(list_prediction)
    #creare una tabella 2x2 con i risultati della classificazione in modo da calcolare
    #true positive / false positive..., oppure posso calcolarli direttamente ricordandomi cosa sono...
    return right_label_class


import copy
def CV(data,matrix):

    num_folds=5
    subset_dim=int(len(data)/num_folds)
    error=[]
    conf_matrix=[]
    for i in range(num_folds):
        dataset = copy.deepcopy(data)
        test_subset = dataset[i * subset_dim:][:subset_dim]
        train_subset =[s for s in dataset if s not in test_subset]
        if (matrix == "no"):
            accuracy=performance(train_subset, test_subset,conf_matrix="no")
            error.append(1-accuracy)
        else:
            conf_matrix.append(performance(train_subset, test_subset, conf_matrix="yes"))
    if(matrix=="no"):
        return sum(error)/len(error)
    else:
        return conf_matrix


# b=CV(my_data_aritmia_clean[:350],matrix="no")
# print(b)



