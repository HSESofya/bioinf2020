# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 22:09:14 2020

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




# находим сумму всех расстояний до узлов к n-2 

def dist_sum(matrix):
    n = np.shape(matrix)[1]
    dist = []
    for i in range(n):
        dist.append((np.sum(matrix[i,:i]) + np.sum(matrix[i+1:,i]))/(n - 2))
    return(dist)
    
    
# находим ближайших соседей
    
def M(matrix):
    min_ = 0
    min_i = 0
    min_j = 0
    n = np.shape(matrix)[1]
    for i in range(2, n + 1):
        for j in range(1, i):
            m = matrix[i - 1][j - 1] - dist_sum(matrix)[i - 1] - dist_sum(matrix)[j - 1]
            if m < min_:
                min_ = m
                min_i = i
                min_j = j
    dist1 = round((matrix[min_i - 1][min_j - 1] + dist_sum(matrix)[min_i - 1] - dist_sum(matrix)[min_j - 1])/float(2), 2)
    dist2 = round((matrix[min_i - 1][min_j - 1] + dist_sum(matrix)[min_j - 1] - dist_sum(matrix)[min_i - 1])/float(2), 2)
    return([min_,[min_i,min_j],[dist1, dist2]])
    
    
def new_node(matrix):
    n = np.shape(matrix)[1]
    min_ = min(M(matrix)[1])
    max_ = max(M(matrix)[1])
    column = [0 for i in range(n)]
    row = [0 for i in range(n-1)]
    
    if min_ == 1:
        for i in range(min_+1, n+1):
            column[i-1] = round((matrix[min_-1, i-1] + matrix[i-1, min_-1] + matrix[max_-1, i-1] + matrix[i-1, max_-1] - matrix[max_-1, min_-1])/float(2),2)
    else:
        for i in range(1, min_):
            row[i - 1] = round((matrix[min_-1, i-1] + matrix[i-1, min_-1] + matrix[max_-1, i-1] + matrix[i-1, max_-1] - matrix[max_-1, min_-1])/float(2), 2)
        for i in range(min_+1, n+1):
            column[i-1] = round((matrix[min_-1, i-1] + matrix[i-1, min_-1] + matrix[max_-1, i-1] + matrix[i-1, max_-1] - matrix[max_-1, min_-1])/float(2), 2)
    del column[max_-1]
    return([row,column])
    
    
# пересчитываем матрицу расстояний с новым узлом
    
def new_distance(matrix):
    matrix_ = matrix.copy()
    max_ = max(M(matrix)[1])
    min_ = min(M(matrix)[1])
    n = np.shape(matrix)[1]
    
    matrix_ = np.delete(matrix_,max_-1, 1)
    matrix_ = np.delete(matrix_, max_-1, 0)
    
    matrix_[min_-1,:n-1] = new_node(matrix)[0]
    matrix_[:n-1, min_-1] = new_node(matrix)[1]
    return(matrix_)
    
    
def print_tree(matrix, leaves):
    tree = leaves.copy()
    m = matrix.copy()
    n = np.shape(m)[1]
    while n > 2:
        w1 = M(m)[1]
        w2 = M(m)[2]
        min_ = min(w1)
        max_ = max(w1)
        y  = []
        if type(tree[w1[0] - 1]) == str:
            y.append([tree[w1[0] - 1], w2[0]])
        else:
            y.append(tree[w1[0] - 1])
        if type(tree[w1[1] - 1]) == str:
            y.append([tree[w1[1] - 1], w2[1]])
        else:
            y.append(tree[w1[1] - 1])
        tree[min_-1] = y
        del tree[max_ - 1]
        m = new_distance(m)
        n = np.shape(m)[1]

    if type(tree[0])== str:
        tree[0] = [tree[0],m[1, 0]]
    if type(tree[1])== str:
        tree[1] = [tree[1],m[1, 0]]
        
    return(tree)
    
print("Введите номер теста:")
test_num = int(input())
print("Матрица расстояний:")
if test_num == 1:
    print(test1)
    print("Результат алгоритма NJ:")
    result = print_tree(test1, leaves1)
    str_result = str(result)
    str_result = str_result.replace("[","(")
    str_result = str_result.replace("]",")")
    str_result = str_result.replace("'","")   
    print(str_result)
    
elif test_num == 2:
    print(test2)
    print("Результат алгоритма NJ:")
    result = str(print_tree(test2, leaves2))
    str_result = str(result)
    str_result = str_result.replace("[","(")
    str_result = str_result.replace("]",")")
    str_result = str_result.replace("'","")
    print(str_result)
    
else:
    print("Ошибка. Доступны тест1 и тест2.")