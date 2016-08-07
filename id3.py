
from math import *
import operator
from dataImport import *
# def entropy(data):
#     entries = len(data)
#     labels = {}
#     for feat in data:
#         label = feat[-1]
#         if label not in labels.keys():
#             labels[label] = 0
#             labels[label] += 1
#     entropy = 0.0
#     for key in labels:
#         probability = float(labels[key])/entries
#         entropy -= probability * log(probability,2)
#     return entropy


my_data_aritmia_clean=[line for line in my_data_aritmia_clean_quasi if len(line)==94]

def col_of_dataset(rows,col):
    new_list=[]
    for i in range(0,len(rows)):
        new_list.append(rows[i][col])
    return new_list

def uniquecounts(rows):
    results={}

    for i in rows:
        a=i[len(i)-1]
        if a not in results: results[a]=0
        results[a]=results[a]+1
    return results

def entropy(rows):
    ent=0.0
    result=uniquecounts(rows)
    if(len(rows)==0): return 0
    else:
        for i in result.keys():
            p=result[i]/len(rows)
            ent=-(p* log(p,2)-ent)
    return ent

def key_to_int(dict_key):
    for i in dict_key:
        a = i
        return a

#split viene usato in due modi diversi: nel caso della costruzione dell'albero in tree
#viene usato per valutare la chiave( che è una stringa fatta in questo modo "<30") nel caso
#della funzione choose(data) split viene usata per dividere il dataset sul valore dati( che sono ancora float)
def split(data, axis, val):
    newData = []
    if(isinstance(val, str)): #usata nella costruzione dell'albero e in choose per i dati categoriali
        for feat in data:
            if  feat[axis] == val:
                reducedFeat = feat[:axis]
                reducedFeat.extend(feat[axis+1:])
                newData.append(reducedFeat)
        return newData
    else:
        for feat in data:
            if feat[axis] >= val:
                reducedFeat = feat[:axis]
                reducedFeat.extend(feat[axis + 1:])
                newData.append(reducedFeat)
        return newData

def split2(data, axis, val):
    if(isinstance(val,float)):
        newData = []
        for feat in data:
            if feat[axis] < val:
                reducedFeat = feat[:axis]
                reducedFeat.extend(feat[axis + 1:])
                newData.append(reducedFeat)
        return newData

    if("<" in val):
        integer_val=float(val.split("<")[1])
        newData = []
        for feat in data:
            if feat[axis] < integer_val:
                reducedFeat = feat[:axis]
                reducedFeat.extend(feat[axis + 1:])
                newData.append(reducedFeat)
        return newData
    else:
        integer_val = float(val.split(">")[1])
        newData = []
        for feat in data:
            if feat[axis] > integer_val:
                reducedFeat = feat[:axis]
                reducedFeat.extend(feat[axis + 1:])
                newData.append(reducedFeat)
        return newData


def keywithmaxval(d):
    dict_to_return = {}
    v = list(d.values())
    k = list(d.keys())
    a = k[v.index(max(v))]
    dict_to_return[a] = max(v)
    return dict_to_return

def infgain(rows,k): #inf gain che utilizzaimo per lo split dei dati float. devo andare a trovare
    #il valore per discretizzare i dati continui
    inf_gain_dict = {}
    i = 0
    featList = [ex[k] for ex in rows]
    attr = set(featList)

    for i in attr:
        set1 = split(rows,k,i )
        set2 = split2(rows,k, i)
        p = float(len(set1)) / len(rows)
        inf_gain_dict[i] = entropy(rows) - p * entropy(set1) - (1 - p) * entropy(set2)

    if (len(inf_gain_dict) == 0):
        inf_gain_dict["key0"] = 0
    if (any(v > 0.0 for v in inf_gain_dict.values())):
        return (keywithmaxval(inf_gain_dict),k)
    else:
        return (inf_gain_dict,k)

def choose(data):
    j=0
    features = len(data[0]) - 1
    baseEntropy = entropy(data)
    bestInfoGain = 0.0

    for i in range(features):
        featList = [ex[i] for ex in data]
        uniqueVals = set(featList)
        newEntropy = 0.0
        if (any(isinstance(v, str) for v in uniqueVals)):
            for value in uniqueVals:
                newData = split(data, i, value)
                probability = (len(newData)) / float(len(data))
                newEntropy += probability * entropy(newData)
        if (any(isinstance(v, float) for v in uniqueVals)):  # da cambiare in float sul dataset vero
            best_gain=infgain(data,i)
            for j in range(0,2):
                if(j==1):
                    newData = split2(data, best_gain[1], key_to_int(best_gain[0].keys()))
                if(j==0):
                    newData = split(data, best_gain[1], key_to_int(best_gain[0].keys()))
                probability = (len(newData)) / float(len(data))
                newEntropy += probability * entropy(newData)

        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            if(j==1):
                bestFeat=(i,key_to_int(best_gain[0].keys()))
            else:
                bestFeat=i

    return bestFeat

def majority(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]



def tree(data,labels):
    if(len(data)==0): # se rimango con i dati vuoti, cambio il nodo in una foglia con classificazione determinata da majority
        return majority(labels)
    classList = [ex[-1] for ex in data]#negative index meaning you count on the right so [-1] is the last element
    if classList.count(classList[0]) == len(classList): #caso in cui siamo arrivati alla fine dell'albero e le istanze
        #sono tutte della stessa classe, restituisco quella classe
        return classList[0]
    if len(data[0]) == 1: #(probabilmente) non ci sono esempi nel subset, nel parent set mancano valori per quel dato valore attributo
        return majority(classList)
    bestFeat = choose(data)
    #bestFeatLabel = labels[bestFeat]
    if(isinstance(bestFeat,int)):
        theTree = {bestFeat:{}}
    #del(labels[bestFeat])
        featValues = [ex[bestFeat] for ex in data]
        uniqueVals = set(featValues)
    else:
        bestFeatString=">"+str(bestFeat[1])
        bestFeatStringOpp="<"+str(bestFeat[1])
        uniqueVals=(bestFeatString,bestFeatStringOpp)
        theTree = {bestFeat[0]: {}}
    if(isinstance(bestFeat,int) and any(isinstance(v,str) for v in featValues)):
        for value in uniqueVals:
            subLabels = labels[:]
            theTree[bestFeat][value] = tree(split(data, bestFeat, value),subLabels)
    else:
        for value in uniqueVals:
            subLabels = labels[:]
            theTree[bestFeat[0]][value] = tree(split2(data, bestFeat[0], value), subLabels)


    return theTree


def classifying(tree,instance):


    if type(tree) == type({}):
        for k in tree.values():
            for j in k.keys():
                if(not ">" and not ("<" not in j) and any(v==j for v in instance)):
                    instance.remove(j)
                    return classifying(k[j],instance)
                if( ">" in j and instance[key_to_int(tree.keys())]>float(j.split(">")[1])):
                    instance.pop(key_to_int(tree.keys()))
                    return classifying(k[j],instance)
                else:
                    if(">" in j):
                        key_minor_branch="<"+j.split(">")[1]
                        instance.pop(key_to_int(tree.keys()))
                        return classifying(k[key_minor_branch], instance)
                    else:
                        if("<" in j and instance[key_to_int(tree.keys())]>float(j.split("<")[1])):
                            key_major_branch = ">" + j.split("<")[1]
                            instance.pop(key_to_int(tree.keys()))
                            return classifying(k[key_major_branch], instance)

                        else:
                            instance.pop(key_to_int(tree.keys()))
                            return classifying(k[j], instance)

    else:
        return tree















