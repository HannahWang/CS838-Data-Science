#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 16:42:04 2018

@author: kangyanghui
"""

# List of POS tags
nnList = ['NN', 'NNP', 'NNPS', 'NNS']  # nouns: breakfast, nuts
adjList = ['JJ', 'VBD', 'JJR', 'JJS']  # adjectives: oiled, cheaper, first, tasty
vbList = ['VB', 'VBG', 'VBP', 'VBP', 'VBZ']  # verb: had, like, am, ordered
prnList = ['PRP','PRP$','POS']  # pronouns: her, my, ours, 's
prp_cjList = ['CC','IN']  # preposition and conjuction: in, for, or, nor, vs. among, by
punctList = ['$', "'", '(', ')', ',', '--', '.', ':', 'SYM','``']  # punctuation and symbols

# List of food ingrediants
ingrdList = ["chicken","pork","beef","duck","steak","shrimp","lamb","fish", \
             "pumpkin","hummus","ham","hams","bacon","salami","orange"\
             "chocolate","latte","lattes","vanilla","bread","ranch","cake", \
             "cheese","egg","eggs","omelette","omelettes","waffle","bread", \
             "pancake","pancakes","potato","potatoes","spanich","lettuce","tomato"\
             "coffee","sandwich","maple","sausage","bagel"]
foodAdjList = ['special','house','thin-cut','fried','french','chile-braised',\
               'daily','american','mexican','sweet','real','orange',\
               'diced','grilled','roasted','shredded','rustic','mixed']

# List of meal names
mealList = ['breakfast','brunch','lunch','dinner','lunches','buffet',\
            'appitizer','appitizers','buffet','beverage','beverages']

# List of correction made to njtk pos tag
# some nouns are treated as adjective or verb
corrToNN = ['breakfast', 'brunch', 'syrup', 'cheese', 'lunch', 'pancakes', \
            'eggs', 'salad', 'cake', 'chocolate', 'greens', 'scramble', \
            'dried', 'sun', 'lattes', 'latte','dinner','pumpkin','ham', \
            'egg','sandwich','pesto','orange','scrambler','jelly','chicken',\
            'feta','benedict','ranch','cranberry']
corrToJJ = ['hot','poached','toasted','roasted','fried','sliced','grilled',\
            'scrambled','pulled','yellow','cozy','excellent','roommy',\
            'savory','arrival','spicy','roomy']
corrToVB = ['order','come','wait','arrived','got','re','was','were','ordered',\
            'tried','had','fear','saw','ask','sit','sat','serve']
corrToRB = ['especially']

# List of common non-food nouns
nonFoodList = ['people', 'place', 'food', 'friends', 'capital', 'wife', \
               'kitchen', 'hotel', 'room', 'madison', 'service', 'outlets', \
               'streets', 'parking', 'times', 'restaurant', 'effort', 'counter', \
               'register', 'day', 'price', 'quality', 'friendly', 'capital', \
               'clean', 'restrooms', 'line', 'party', 'selections', 'chicago', \
               'capitol', 'review', 'reviews', 'crowds', 'staff', 'range', \
               'time', 'minute', 'minutes', 'thing','tables','table','husband',\
               'morning', 'friday', 'monday', 'tuesday', 'thursday', 'wednesday',\
               'sunday', 'saturday', 'number', 'system', 'menu', 'vibe','looks',\
               'diner', 'prize', 'visitors', 'friends', 'weekends', 'everyone',\
               'door', 'option', 'options', 'yummy', 'yum', 'decison','days',\
               'travel','fun', 'weekend', 'thing', 'things', 'reason', 'mad', \
               'tight', 'smiles', 'week', 'first', 'meeting', 'buisiness', \
               'yelp', 'average', 'atmosphere', 'flight', 'old', 'uw', \
               'student', 'students', 'others', 'square', 'market', 'feel', \
               'game', 'changer', 'stop', 'st', 'woman', 'women', 'man', \
               'men', 'mornings', 'item', 'items', 'portion', 'portions',\
               'lines', 'downtown', 'someone', 'employees', 'exprience',\
               'friend', 'friends', 'customer', 'year', 'years', 'month',\
               'months', 'everything', 'places', 'summer', 'winter', \
               'fall', 'january', 'feburary', 'march', 'april', 'may', 'june', \
               'july', 'august', 'september', 'october', 'november', 'december',\
               'tummies', 'ta', 'noon', 'weather', 'state', 'street', 'campus',\
               'block', 'business', 'group', 'town', 'inn', 'nothing', 'daughter',\
               'son', 'family', 'families', 'guy', 'guys', 'couple', 'couples',\
               'afternoon', 'evening', 'place', 'places', 'today','door','doors'\
               'vehicle', 'car', 'cars', 'noon', 'building', 'experience', \
               'trip', 'resturant', 'years', 'hours', 'minutes', 'seat', 'waiter',\
               'spot', 'tip', 'color', 'colors', 'work', 'crowd', 'team','go',\
               'recommendation', 'few', 'nice', 'corner','cozy','caf','t','did',\
               'n','disappointment','frustration','stuff','small','big','tends',\
               'walk','run','move','lot','indoor','fair','cause','anyone','wow',\
               'excellent','best','better','great','boy','opening','menus','half',\
               'wow','rush','spots','most','whites','waitstaff','life','talk',\
               'dennys','ihop','style','ages','prices','price','saturdays','sundays',\
               'good','classic','resturants','professionals','delicious','savory',\
               'half','opening','amount','friendliness','killer','capacity',\
               'wonderful','much','awesome','creative','local','hype','worst',\
               'city','hall','wi-fi','turnover']
