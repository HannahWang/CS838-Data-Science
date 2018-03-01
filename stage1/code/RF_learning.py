#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_recall_fscore_support
import pandas as pd


df1 = pd.read_csv('/Users/yyc/Desktop/learning/processed_I.csv')
df2 = pd.read_csv('/Users/yyc/Desktop/learning/processed_J.csv')

"""
X_train = df1.iloc[1:, 4:]
y_train = df1.iloc[1:,2]

X_test = df2.iloc[1:, 4:]
y_test = df2.iloc[1:,2]

"""
X_train = df1.iloc[1:, [3, 4, 5, 6, 7, 8, 9, 12, 13, 18, 20, 22, 25, 26, 38, 39, 46, 51, 52, 64]]
y_train = df1.iloc[1:,2]

X_test = df2.iloc[1:, [3, 4, 5, 6, 7, 8, 9, 12, 13, 18, 20, 22, 25, 26, 38, 39, 46, 51, 52, 64]]
y_test = df2.iloc[1:,2]




max_precision = 0
recall_atMax = 0
f1_atMax = 0
max_recall= 0
precision_atMax = 0
f1_atMax2 = 0
max_i = 0
max_j = 0
max_k = 0
ri = 0; rj = 0; rk = 0

precision_90 = 0
recall_60 = 0
f1_good = 0
pi = 0; pj = 0; pk = 0
for i in range(2, 18):
    for j in range(2, 18):
        for k in range(2,18):
            clf = RandomForestClassifier(max_depth=i, n_estimators=j, max_features=k)

            clf.fit(X_train, y_train)
            y_predict = clf.predict(X_test)
            precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_predict, average='binary')
            if recall > max_recall or (recall == max_recall and precision > precision_atMax):
                max_recall = recall
                precision_atMax = precision
                f1_atMax2 = f1
                ri = i
                rj = j
                rk = k
                
            if precision >= 0.9 and recall >= 0.6:
                if precision > precision_90:
                    precision_90 = precision
                    recall_60 = recall
                    f1_good = f1
                    pi = i
                    pj = j
                    pk = k
                
            if precision > max_precision or (precision == max_precision and recall > recall_atMax):
                max_precision = precision
                recall_atMax = recall
                f1_atMax = f1
                max_i = i
                max_j = j
                max_k = k
                
            #print("max_depth: %d, n_estimators: %d, max_features: %d" % (i, j, k))
            #print("precision: %0.4f, recall: %0.4f, f1: %0.4f" % (precision, recall, f1))

print("max_precision: %0.4f, recall: %0.4f, f1: %0.4f" % (max_precision, recall_atMax, f1_atMax))
print("max_i: %d, max_j: %d, max_k: %d" % (max_i, max_j, max_k))
print("precision: %0.4f, max_recall: %0.4f, f1: %0.4f" % (precision_atMax, max_recall, f1_atMax2))
print("r_i: %d, r_j: %d, r_k: %d" % (ri, rj, rk))
print("precision_90: %0.4f, recall_60: %0.4f, f1: %0.4f" % (precision_90, recall_60, f1_good))
print("r_i: %d, r_j: %d, r_k: %d" % (pi, pj, pk))



