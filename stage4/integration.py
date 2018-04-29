#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:50:07 2018

Integrate table A (yelp) and Table B (tripadvisor)
Create table E containing resturants entities and their info from yelp and tripadvisor

@author: kangyanghui
"""

import py_entitymatching as em
import pandas as pd

#%% Matching tuples

# read tables
A = em.read_csv_metadata('A.csv', key='id')
B = em.read_csv_metadata('B.csv', key='id')

# Load blocked data pairs
C = em.read_csv_metadata('C.csv', key='_id', 
                         ltable=A, rtable=B, fk_ltable='ltable_id', fk_rtable='rtable_id')

# Load the labeled data
G = em.read_csv_metadata('S_labeled.csv', key='_id', 
                         ltable=A, rtable=B, fk_ltable='ltable_id', fk_rtable='rtable_id')

# Generate a set of features
F = em.get_features_for_matching(A.iloc[:, 1:8], B.iloc[:, 1:8], validate_inferred_attr_types=False)

# Create a feature on the value of (price + rating), then compute Levenshtein similarity
sim = em.get_sim_funs_for_matching()
tok = em.get_tokenizers_for_matching()
feature_string = """lev_sim(wspace(float(ltuple['price']) + float(ltuple['rating'])), 
                            wspace(float(rtuple['price']) + float(rtuple['rating'])))"""
feature = em.get_feature_fn(feature_string, sim, tok)

# Add feature to F
em.add_feature(F, 'lev_ws_price+rating', feature)

# Convert the sample set into a set of feature vectors using F
H = em.extract_feature_vecs(G, 
                            feature_table=F, 
                            attrs_after='labe',
                            show_progress=False)

# impute missing values
H = em.impute_table(H, 
                exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'labe'],
                strategy='mean')

# Fit a Naive Bayes matcher
matcher = em.NBMatcher(name='NaiveBayes')
matcher.fit(table=H, 
       exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'labe'], 
       target_attr='labe')

# Apply matcher to the whole dataset
Ht = em.extract_feature_vecs(C, 
                            feature_table=F,
                            show_progress=False)
Ht = em.impute_table(Ht, 
                exclude_attrs=['_id', 'ltable_id', 'rtable_id'],
                strategy='mean')
predictions = matcher.predict(table=Ht, exclude_attrs=['_id', 'ltable_id', 'rtable_id'], 
              append=True, target_attr='predicted', inplace=False)

# save the final predictions
predictions.to_csv('P.csv', index = False)

#%% get only the positive paris
P = predictions[predictions['predicted'] == 1]

# Add columns to E
E0 = P[['_id','ltable_id','rtable_id']]
E1 = pd.merge(E0, A, how = 'left', left_on = 'ltable_id', right_on = 'id')
E2 = pd.merge(E1, B, how = 'left', left_on = 'rtable_id', right_on = 'id',
              suffixes = ['_a','_b'])

# fill na: use hours of b to fill hours of a
E2.isnull().sum()
for i in range(14, 28, 1):
    E2.iloc[:,i] = E2.iloc[:,i].fillna(E2.iloc[:,i+25])
E2.isnull().sum()

E2['city'] = E2['city_b']
E2['category_1'] = E2['category_1_b']
E2['category_2'] = E2['category_2_b']
E2['category_3'] = E2['category_1_a']
E2['category_4'] = E2['category_2_a']
E2 = E2.drop(E2.columns[range(39, 53, 1)], axis = 1)
E2 = E2.drop(columns = ['ltable_id','rtable_id','category_1_a','category_2_a','category_1_b',
                        'category_2_b','city_a','city_b','address_b','zipcode_b',
                        'phone_b'])

# reorder columns
colindex = [0,1,23,2,24,28,4,3,5,29,30,31,32,6,7,8,25,26,27]
colindex.extend(range(9,23,1))
E = E2.iloc[:,colindex]

# rename some column names
colrelist = [6, 7, 8]
colrelist.extend(range(19, 33, 1))
colnames = []
for i in range(E.shape[1]):
    if i in colrelist:
        coln = E.columns[i][0:-2]
    else:
        coln = E.columns[i]
    colnames.append(coln)

E.columns = colnames

E.to_csv('E.csv', index = False)
