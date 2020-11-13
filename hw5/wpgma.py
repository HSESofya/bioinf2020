# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 18:05:38 2020

@author: sofya
"""
import numpy as np 

test1 = []
with open('test1.txt') as f:
    test1 = [[x for x in line.split()] for line in f]       
test1 = np.asarray(test1)
test1 = test1.astype(np.float)
length1 = len(test1)
leaves1 = ["A", "B", "C", "D"]

test2 = []
with open('test2.txt') as f:
    test2 = [[x for x in line.split()] for line in f]       
test2 = np.asarray(test2)
test2 = test2.astype(np.float)
length2 = len(test2)
leaves2 = ["A", "B", "C", "D", "E", "F"]



def min_ij(matrix):
    min_i = 0
    min_j = 0
    min_ = np.inf
    
    for i in range(len(matrix)):
        temp = matrix[i]
        mask = np.nonzero(temp)
        min_temp = min(temp[mask])
        j = temp.tolist().index(min_temp)
        if min_temp < min_: 
            min_i = i
            min_j = j
            min_ = min_temp
    return min_i, min_j


def tree_print(dictionary,finalCluster):
    stack = []
    result = []
    stack.append(finalCluster)
    prev = 0
    while stack:
        curr = stack.pop()
        if isinstance(curr, float):
            if isinstance(prev, float):
                result.pop()
                result.append(")")
            result.append(":"+str(curr))
            result.append(",")
            
        elif curr in dictionary.keys():
        
            stack.append(dictionary[curr][0])
            stack.append(dictionary[curr][1])
            stack.append(dictionary[curr][2])
            stack.append(dictionary[curr][3])
            result.append("(")
        else:
            result.append(curr)
        prev = curr
        
    result.pop()
    result.append(")")  
    result.append(";")  
    return result


def wpgma(matrix, length,dictionary, leaves_num):
    leaves = []
    count = 0
    
    for i in range(0, length): 
        leaves.append(leaves_num[i])
    numberOfClusters = i+1
    
    while(length>1):
        
        numberOfClusters += 1
        count += 1
        min_i,min_j = min_ij(matrix)
        
        leaves.append("seq"+str(numberOfClusters)) 
        dist = round(matrix[min_i][min_j]/2,2)
        
        size = 0
        if leaves[min_i] not in dictionary.keys():
            size = 1
            dist1 = dist
        else:
            size = dictionary[leaves[min_i]][4]
            dist1 = dist - max(dictionary[leaves[min_i]][0],dictionary[leaves[min_i]][2])
        
        if leaves[min_j] not in dictionary.keys():
            size += 1
            dist2 = dist
        else:
            size += dictionary[leaves[min_j]][4]
            dist2 = dist - max(dictionary[leaves[min_j]][0],dictionary[leaves[min_j]][2])
        dictionary["seq"+str(numberOfClusters)] = [dist1,leaves[min_i],dist2,leaves[min_j],size]
        
        # Create a new row and column
        matrix = np.insert(matrix, length, values=0, axis=0)
        matrix = np.insert(matrix, length, values=0, axis=1)

        for i in range(0, length):
            matrix[-1][i] = (matrix[i][min_i] + matrix[i][min_j])/2
            matrix[i][-1] = (matrix[i][min_i] + matrix[i][min_j])/2
            
            
        # Delete the minimum value
        if min_i < min_j:
            matrix = np.delete(matrix, min_i, 0)
            matrix = np.delete(matrix, min_i, 1)
            matrix = np.delete(matrix, min_j-1, 0)
            matrix = np.delete(matrix, min_j-1, 1)
            length = len(matrix)
            del leaves[min_j]
            del leaves[min_i]

        else:
            matrix = np.delete(matrix, min_i, 0)
            matrix = np.delete(matrix, min_i, 1)
            matrix = np.delete(matrix, min_j, 0)
            matrix = np.delete(matrix, min_j, 1)            
            length = len(matrix)
            del leaves[min_i]
            del leaves[min_j]
            
    return "seq"+str(numberOfClusters)


def upgma(matrix, length,dictionary, leaves_num):
    leaves = []
    count = 0
    for i in range(0, length):
        leaves.append(leaves_num[i])
    numberOfClusters = i+1
    
    while length > 1:
        numberOfClusters += 1
        count += 1
        min_i, min_j = min_ij(matrix)
        leaves.append("seq" + str(numberOfClusters))  
        dist = matrix[min_i][min_j]/2
        dist = round(dist, 2)

        if leaves[min_i] not in dictionary.keys():
            size1 = 1
            dist1 = dist
        else:
            size1 = dictionary[leaves[min_i]][4]
            dist1 = round(dist - max(dictionary[leaves[min_i]][0], dictionary[leaves[min_i]][2]),2)
        
        if leaves[min_j] not in dictionary.keys():
            size2 = 1
            dist2 = dist
        else:
            size2 = dictionary[leaves[min_j]][4]
            dist2 = round(dist - max(dictionary[leaves[min_j]][0],dictionary[leaves[min_j]][2]), 2)
        dictionary["seq" + str(numberOfClusters)] = [dist1, leaves[min_i], dist2, leaves[min_j], size1+size2]
        
        # Добавляем новую строку и столбец
        matrix = np.insert(matrix, length, values = 0, axis = 0)
        matrix = np.insert(matrix, length, values = 0, axis = 1)
        
        for i in range(length):
            matrix[-1][i] = matrix[i][-1] = (size1*matrix[i][min_i] + size2*matrix[i][min_j])/(size1+size2)
        
        # Delete the minimum value
        if min_i < min_j:
            matrix = np.delete(matrix, min_i, 0)
            matrix = np.delete(matrix, min_i, 1)
            matrix = np.delete(matrix, (min_j)-1, 0)
            matrix = np.delete(matrix, (min_j)-1, 1)
            length = len(matrix)
            del leaves[min_j]
            del leaves[min_i]

        else:
            matrix = np.delete(matrix, min_i, 0)
            matrix = np.delete(matrix, min_i, 1)
            matrix = np.delete(matrix, min_j, 0)
            matrix = np.delete(matrix, min_j, 1)            
            length = len(matrix)
            del leaves[min_i]
            del leaves[min_j]
        
    return "seq"+str(numberOfClusters)


dict_ = {}
print("Введите номер теста:")
test_num = int(input())

if test_num == 1:
    print("Матрица расстояний:")
    print(test1)
    print("Результат алгоритма UPGMA:")
    result = tree_print(dict_, upgma(test1, length1, dict_, leaves1))
    result = ''.join(result)
    print(result)
    
    print("Результат алгоритма WPGMA:")
    result2 = tree_print(dict_, wpgma(test1, length1, dict_, leaves1))
    result2 = ''.join(result2)
    print(result2)
    
elif test_num == 2:
    print("Матрица расстояний:")
    print(test2)
    print("Результат алгоритма UPGMA:")
    result = tree_print(dict_, upgma(test2, length2, dict_, leaves2))
    result = ''.join(result)
    print(result)
    
    print("Результат алгоритма WPGMA:")
    result2 = tree_print(dict_, wpgma(test2, length2, dict_, leaves2))
    result2 = ''.join(result2)
    print(result2)  
else:
    print("Ошибка. Доступны тест1 и тест2.")
