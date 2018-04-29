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

#%% Merge columns to Table A and B
# get only the positive paris
predictions = pd.read_csv('P.csv')
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

# remove duplicated rows based on id of Table A
E2 = E2.drop_duplicates(subset = 'id_a')

# merge the category columns
# define two categories:
# category_loc: category by location
# category_food: category by food
cat_loc = ['american','japanese','mexican','italian','thai','chinese','korean',
           'vietnamese','mediterranean','french','indian','brazilian']
cat_food = ['barbecue','pizza','cafe','seafood','steakhouse','fast food','sushi',
            'ramen','breakfast & brunch','burger','bars']

E2['categories'] = E2[['category_1_b','category_2_b','category_1_a',
                       'category_2_a']].values.tolist()

def get_category_loc(row):
    """get the category based on ranked list of category_by_location
    """
    cat = 'other'
    for t in cat_loc:
        for item in row:
            if pd.isnull(item):
                continue
            if item.split()[0].lower() == 'american':
                return 'american'
            if item.lower() == 'pizza':
                return 'italian'
            if item.lower() == 'ramen':
                return 'japanese'
            if em.lev_dist(item.lower(), t) < 2:
                return t
    return cat

def get_category_food(row):
    """get the category based on a ranked list of food category
    """
    cat = 'other'
    for t in cat_food:
        for item in row:
            if pd.isnull(item):
                continue
            if item.split()[0].lower() == 'sushi':
                return 'sushi'
            if em.lev_dist(item.lower(), t) < 2:
                return t
    return cat

def add_asian_other(row):
    """Create a new category called "asian other"
    """
    if row['category'] == 'other':
        for cat in row['categories']:
            if pd.isnull(cat):
                continue
            for x in cat.split():
                if x.lower() == 'asian':
                    return 'asian other'
    return row['category']


E2['category_loc'] = E2['categories'].apply(get_category_loc)
E2['category_food'] = E2['categories'].apply(get_category_food)

# combine into a single category based primary on food, fill with location
E2['category'] = E2['category_food']
E2.loc[E2['category_food'] == 'other', 'category'] = E2.loc[E2['category_food'] == 'other', 'category_loc']

# combine low count categories
E2['category'] = E2['category'].replace({'ramen':'japanese','brazilian':'other',
                                         'french':'other','indian':'asian other'})
E2['category'] = E2.apply(add_asian_other, axis = 1)
    
Et = E2[['categories','category_loc','category_food','category']]
E2.category_loc.value_counts()
E2.category_food.value_counts()
E2.category.value_counts()


#%% Clean columns

# reorder columns
colindex = [0,3,28,4,29,33,9,7,10,56,54,55,11,12,13,36,37,38]
colindex.extend(range(13,28,1))
E = E2.iloc[:,colindex]

# rename some column names
colrelist = [5, 6, 7, 8]
colrelist.extend(range(19, 33, 1))
colnames = []
for i in range(E.shape[1]):
    if i in colrelist:
        coln = E.columns[i][0:-2]
    else:
        coln = E.columns[i]
    colnames.append(coln)

E.columns = colnames
E = E.rename(columns = {'price_a':'price_yelp','rating_a':'rating_yelp',
                        'review_count_a':'review_count_yelp',
                        'price_b':'price_trip','rating_b':'rating_trip',
                        'review_count_b':'review_count_trip',
                        'name_b':'name'})

E = E.drop(columns = ['_id','name_a'])

E.to_csv('E.csv', index = False)
