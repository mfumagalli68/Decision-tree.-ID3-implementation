# import csv
# file_path_name="C:/Users/mauro/Dropbox/Machine Learning Project/Dataset papabile/Life science-Heart disease/Aritmia.data"
# file_name="Aritmia.data"
# my_data_aritmia=[]
# with open(file_path_name, 'r') as f:
#    for line in f:
#        provisory_list=line.strip() .split(",")
#        my_data_aritmia.append(provisory_list)
#
# #data manipulation: convertire in float,cambiare il target, convertire sex in female , male
# def int_to_float(cell):
#   try:
#       cell=float(cell)
#   except ValueError:
#       pass
#   return cell
#
# for i in range(0, len(my_data_aritmia)):
#     for j in range(0,len(my_data_aritmia[i])):
#             my_data_aritmia[i][j]=int_to_float(my_data_aritmia[i][j])
#
# for i in range(0, len(my_data_aritmia)):
#     if my_data_aritmia[i][279]>1:
#         my_data_aritmia[i][279]=0.0
#
# for i in range(0, len(my_data_aritmia)):
#     if(my_data_aritmia[i][1]==1):
#         my_data_aritmia[i][1]="female"
#     else:
#         my_data_aritmia[i][1]="male"
#
#
# #function to substituite all dummy variable with yes and no
# def column(nestedlist, i):
#     return [row[i] for row in nestedlist]
#
# for j in range(0,(len(my_data_aritmia[0])-1)):
#     col_to_analyze=column(my_data_aritmia,j)
#     #how to say that vec
#     if(all(isinstance(v,float) for v in col_to_analyze) and all(v<=1 for v in col_to_analyze) ):
#         for i in range(0,len(col_to_analyze)):
#             if(col_to_analyze[i]==1):
#                 col_to_analyze[i]="yes"
#             else:
#                 col_to_analyze[i]="no"
#
#         for k in range(0,len(my_data_aritmia)):
#             my_data_aritmia[k][j]=col_to_analyze[k]


def int_to_float(cell):
  try:
      cell=float(cell)
  except ValueError:
      pass
  return cell

file_path_name="C:/Users/mauro/Dropbox/Machine Learning Project/Dataset papabile/Life science-Heart disease/DatasetCleaned.csv"
file_name="DatasetCleaned.csv"
my_data_aritmia2=[]
with open(file_path_name, 'r') as f:
   for line in f:
       provisory_list2=line.strip() .split(",")
       my_data_aritmia2.append(provisory_list2)
for i in range(0, len(my_data_aritmia2)):
    for j in range(0,len(my_data_aritmia2[i])):
            my_data_aritmia2[i][j]=int_to_float(my_data_aritmia2[i][j])

#print(my_data_aritmia2)
my_data_aritmia_clean_quasi=[line for line in my_data_aritmia2 if ("?" not in line)]

# count=0
# count1=0
# for v in range(0,len(my_data_aritmia_clean_quasi)):
#     if(len(my_data_aritmia_clean_quasi[v])==94):
#         count=count+1
#     else:
#         count1=count1+1
#
# print(count)
# print(count1)