#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin
from sklearn import preprocessing


class DataFrameImputer(TransformerMixin):

    def __init__(self):
        """
        Impute missing values.
        Columns of dtype object are imputed with the most frequent value 
        in column.
        Columns of other types are imputed with mean of column.
        """
    def fit(self, X, y=None):

        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
            index=X.columns)

        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)

# combine training and test dataset
df1 = pd.read_csv('/Users/yyc/Desktop/learning/set_I_examples.csv')
df2 = pd.read_csv('/Users/yyc/Desktop/learning/set_J_examples.csv')
df3 = df1.append(df2)

# impute missing values
df3_t = DataFrameImputer().fit_transform(df3)

# label encode
le = preprocessing.LabelEncoder()

# transform label
df3_t.iloc[:, 1] = le.fit_transform(df3_t.iloc[:,1])

for i in range(2, len(df3.iloc[0, :])):
    df3_t.iloc[:, i] = le.fit_transform(df3_t.iloc[:,i])
    
# normalization
scaler = preprocessing.MinMaxScaler()

for i in range(2, len(df3.iloc[0, :])):
    df3_t.iloc[:, i] = scaler.fit_transform(df3_t.iloc[:,i])


train = df3_t.iloc[0:2227, :]
test = df3_t.iloc[2227:, :]

train.to_csv('processed_I.csv', sep=',')
test.to_csv('processed_J.csv', sep=',')   
