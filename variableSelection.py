import math
import scipy.stats as st
import numpy as np
import pandas as pd


def chisqtest(data_attribute,label,col):

    variable_value = []
    flag=0
    # treating missing values. eliminate from variable missing values ("?") and eliminate from label
    # i corrispondenti target per i missing values. faccio ciò  grazie a index, che mi identifica gli indici della lista variable
    # dove ho eliminato i missing values
    if (any(v == "?" for v in data_attribute)):
        index = [i for i in range(0, len(data_attribute)) if data_attribute[i] == "?"]
        data_attribute = [i for i in data_attribute if i != "?"]
        for indice in sorted(index, reverse=True):
            del label[indice]

    for i in data_attribute:
        if i not in variable_value:
            variable_value.append(i)



    if(any(isinstance(v,float) for v in data_attribute)):


        df = pd.DataFrame({'variable': data_attribute, 'target': label})
        totals=pd.crosstab(pd.cut(df['variable'], np.linspace(min(data_attribute),max(data_attribute),4), include_lowest=True), df['target'],margins=True)
        flag=1
    else:
        df = pd.DataFrame({'variable': data_attribute, 'target': label})
        totals = pd.crosstab(df['variable'], df['target'], margins=True).reset_index()

    vector_number_total_case=totals.values[len(totals.values)-1]
    N=vector_number_total_case[len(vector_number_total_case)-1]
    stat_test= []
    for i in range(0,len(totals.values)-1):
        for j in range(1,len(totals.values[i])-1):
            expected=totals.values[i][len(totals.values[i])-1]*totals.values[len(totals.values)-1][j]/N
            stat_test.append((expected-totals.values[i][j])**2/expected)

    statistic=sum(stat_test)
    if(flag==0):
        pvalue=1-st.chi2.cdf(statistic, df=((len(variable_value)-1)*(1)))
    else:
        pvalue = 1 - st.chi2.cdf(statistic, df=(3 - 1) * (1))#nel caso in cui i dati siano continui e abbia discretizzato

    return statistic,pvalue,col

def subset(data,label,whichset):

    #subsetdata_0=[[i for i in data if data[i][len(data)-1]==1]] da provare...
    subsetdata_1=[]
    subsetdata_0=[]
    for i in range(0,len(label)):
        if(label[i]==1):
            subsetdata_1.append(data[i])
        else:
            subsetdata_0.append(data[i])

    if(whichset=="group0"):
        return subsetdata_0
    else:
        return subsetdata_1

def biserialpearsoncorr(data_attribute,label,col):
    if (any(v == "?" for v in data_attribute)):
        index = [i for i in range(0, len(data_attribute)) if data_attribute[i] == "?"]
        data_attribute = [i for i in data_attribute if i != "?"]
        for indice in sorted(index, reverse=True):  # guarda sorted cosa fa
            del label[indice]

    group_0=subset(data_attribute,label, "group0")
    group_1=subset(data_attribute,label, "group1")
    n1=len(group_0)
    n0=len(group_1)
    n=len(data_attribute)

    data_mean_0=np.mean(np.asarray(group_0))
    data_mean_1=np.mean(np.asarray(group_1))
    data_std=np.std(np.asarray(data_attribute))
    prop_n1=n1/n
    prop_n0=n0/n

    r_pb=((data_mean_0-data_mean_1)*math.sqrt(prop_n1*prop_n0))/data_std

    stat_test=r_pb/math.sqrt(math.fabs(1-r_pb**2)/(n-2))
    p_value=2*(1-st.t.cdf(math.fabs(stat_test),df=(n1+n0-2)))
    return stat_test,p_value,col


##prova da far vedere all'esame + import dati
def col_of_dataset(rows,col):
    new_list=[]
    for i in range(0,len(rows)):
        new_list.append(rows[i][col])
    return new_list

import csv
file_path_name="C:/Users/mauro/Dropbox/Machine Learning Project/Dataset papabile/Life science-Heart disease/Aritmia.data"
file_name="Aritmia.data"
my_data_aritmia=[]
with open(file_path_name, 'r') as f:
   for line in f:
       provisory_list=line.strip() .split(",")
       my_data_aritmia.append(provisory_list)

#data manipulation: convertire in float,cambiare il target, convertire sex in female , male
def int_to_float(cell):
  try:
      cell=float(cell)
  except ValueError:
      pass
  return cell

for i in range(0, len(my_data_aritmia)):
    for j in range(0,len(my_data_aritmia[i])):
            my_data_aritmia[i][j]=int_to_float(my_data_aritmia[i][j])

for i in range(0, len(my_data_aritmia)):
    if my_data_aritmia[i][279]>1:
        my_data_aritmia[i][279]=0.0

for i in range(0, len(my_data_aritmia)):
    if(my_data_aritmia[i][1]==1):
        my_data_aritmia[i][1]="female"
    else:
        my_data_aritmia[i][1]="male"


#function to substituite all dummy variable with yes and no
def column(nestedlist, i):
    return [row[i] for row in nestedlist]

for j in range(0,(len(my_data_aritmia[0])-1)):
    col_to_analyze=column(my_data_aritmia,j)
    #how to say that vec
    if(all(isinstance(v,float) for v in col_to_analyze) and all(v<=1 for v in col_to_analyze) ):
        for i in range(0,len(col_to_analyze)):
            if(col_to_analyze[i]==1):
                col_to_analyze[i]="yes"
            else:
                col_to_analyze[i]="no"

        for k in range(0,len(my_data_aritmia)):
            my_data_aritmia[k][j]=col_to_analyze[k]

#prova
selected_feature=[]

for i in range(0,(len(my_data_aritmia[0])-1)):
    label = [[instance for instance in col[-1:]] for col in my_data_aritmia]
    label = [item for sublist in label for item in sublist]
    my_data_aritmia_attribute=col_of_dataset(my_data_aritmia,i)
    if(any(isinstance(v,str) for v in my_data_aritmia_attribute)):
        res_test=chisqtest(my_data_aritmia_attribute,label,i)
    else:
        res_test = biserialpearsoncorr(my_data_aritmia_attribute, label, i)
    if(res_test[1]<0.05):
        selected_feature.append(res_test)

print(selected_feature)