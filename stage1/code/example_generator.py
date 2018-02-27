#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 17:36:58 2018

Parse and generate attributes for all examples in documents
1) parse each document and extract 1-4 word entities
2) constructe attributes for each entity

Entity attributes:
    

@author: kangyanghui
"""

import unicodedata
import nltk
import os
import glob
import io
import re
import numpy as np
import pandas as pd
import sys
from word_lists import *

def getEntyAttr(wordList, foodList, idx, length):
    """
    Return attributes of current entity starting at word 'i' in wordList with 'length' number of words
    """
    # get entity
    words = [item[0] for item in wordList[idx:(idx+length)]]
    entity = ' '.join(words)
    
    # has food ingredients in the string
    hasFood = False
    hasFoodAdj = False
    for item in wordList[idx:(idx+length)]:
        if item[0].lower() in ingrdList:
            hasFood = True   
        if item[0].lower() in foodAdjList:
            hasFoodAdj = True
    
    # postag related attributes
    hasNN = False  
    hasADJ = False   # has adjectives in the string
    for item in wordList[idx:(idx+length)]:    
        pos = item[1]
        if pos in nnList:
            hasNN = True
        if pos in adjList:
            hasADJ = True
    
    # occurence of comman or semicolon in the sentence
    occur = [i for i, x in enumerate(wordList) if x[0] in [',',';']]  

    # distance to comma or semicolon
    if len(occur) == 0:
        distCS = len(wordList)
    else:
        distCS = min(list(abs((np.asarray(occur) - idx))));              
    
    # attributes of the bag of words
    attributes = {
            'word_0': entity,
            'label': entity in foodList,
            'word_0.hasFood': hasFood,    # has food ingredient in the string
            'word_0.hasFoodAdj': hasFoodAdj,    # has food adjective in the string (e.g. fried)
            'word_0.hasCapital': not entity.islower(),   # has capital letters
            'word_0.hasNN': hasNN,   # has nouns in the string
            'word_0.hasADJ': hasADJ,  # has adjectives in the string
            'word_0.distCS': distCS,   # distance to comman or semicolon
            'word_0.distBG': idx,   # distance to begining of the sentence
            'word_0.distEND': len(wordList) - 1 - idx,   # distance to end of the sentence
            'word_0.length': length   # number of word
            }
    
    return attributes


def getSrrdAttr(attr, word, postag, prefix):
    """
    Append attributes of neighboring 'word' to 'attr'
    """
    attr.update({
        prefix: word.lower(),
        prefix+'.hasCapital': not word.islower(),
        prefix+'.postag': postag,
        prefix+'.isFood': word.lower() in ingrdList,
        prefix+'.isFoodAdj': word.lower() in foodAdjList,
        prefix+'.isMeal': word.lower() in mealList,
        prefix+'.isADJ': postag in adjList, # is adjective
        prefix+'.isNN': postag in nnList,  # is noun
        prefix+'.isNum': postag == 'CD',  # is numeral
        prefix+'.isDT': postag == 'DT',   # is determinter: the, an, a
        prefix+'.isPRN': postag in prnList,   # is pronoun
        prefix+'.isVB': postag in vbList,  # is verb
        prefix+'.isPRCJ': postag in prp_cjList   # is preposition/conjunction
        })
    return attr


def getAttributes(wordList, foodList, idx, length):
    """
    Compile all the attributes of an entity starting at word 'i' in wordList with 'lenght'
    number of words
    """
    # attributes of this word (or words)
    attributes = getEntyAttr(wordList, foodList, idx, length);
    
    # attributes of word-1
    if idx > 0:
        word_l1 = wordList[idx - 1][0]
        postag_l1 = wordList[idx - 1][1]
        attributes = getSrrdAttr(attributes, word_l1, postag_l1, 'word_l1')
    
    # attributes of word-2
    if idx > 1:
        word_l2 = wordList[idx - 2][0]
        postag_l2 = wordList[idx -2][1]
        attributes = getSrrdAttr(attributes, word_l2, postag_l2, 'word_l2')
    
    # attributes of word+1
    if idx < len(wordList) - 1:
        word_r1 = wordList[idx + 1][0]
        postag_r1 = wordList[idx + 1][1]
        attributes = getSrrdAttr(attributes, word_r1, postag_r1, 'word_r1')
        
    # attributes of word+2
    if idx < len(wordList) - 2:
        word_r2 = wordList[idx + 2][0]
        postag_r2 = wordList[idx + 2][1]
        attributes = getSrrdAttr(attributes, word_r2, postag_r2, 'word_r2')
        
    return attributes


def prune(wordList):
    """
    Check if the entity should be removed
    Rules:
        1) one word can only be Noun
        2) multi-word entity only contains noun and adjective
        3) does not include word from 'non-food list'
    """
    valid = True
    if len(wordList) == 1:
        if wordList[0][1] not in nnList:
            valid = False
        if wordList[0][0].lower() in nonFoodList:
            valid = False
    else:
        for item in wordList:
            if (item[1] not in nnList) & (item[1] not in adjList):
                valid = False
            if item[0].lower() in nonFoodList:
                valid = False
#            if item[0].lower() in nonFoodAdjList:
#                valid = False
#        
    return valid


def parseSlash(tokens):
    """
    parse words connected by backslash in a sentence
    this was not handled by nltk toenizer
    """
    words = []
    for tk in tokens:
        parts = re.split('[/.\']', tk)
        words.extend([x for x in parts if len(x) > 0]) 
    return words

def correctTag(wordList):
    """
    correct some nouns that are mistakenly treated as other tag by nltk
    """
    wordListNew = []
    for item in wordList:
        tag = item[1]
        if item[0].lower() in corrToNN:
            tag = 'NN'
        elif item[0].lower() in corrToJJ:
            tag = 'JJ'   
        elif item[0].lower() in corrToVB:
            tag = 'VB'
        elif item[0].lower() in corrToRB:
            tag = 'RB'
        wordListNew.append((item[0], tag))
    return wordListNew


if __name__ == '__main__':
    os.chdir("./markup_v2/set_I")
    files = glob.glob("*.txt")
    
    # split review into sentences
    revSents = []
    for file in files:
        docID = int(file.split('.')[0])
        print(docID)
        f = io.open(file,'r')
        review = f.read()
        sents = unicodedata.normalize('NFKD', review).encode('ascii','ignore')
        sents = nltk.sent_tokenize(sents, language = "english")
        for sent in sents:
            revSents.append((docID, sent))
            
    # for each sentence generate examples of attributes
    allEntities = []
    posCount = 0   # positive entity counts
    posListOrg = []
    for row in revSents:
        docID = row[0]
        sentRaw = row[1]
        
        foodList = re.findall(r'<pos[^>]*>([^<]+)</pos>',sentRaw) # find all tagged food
        sentClean = re.sub(re.compile(r'<.*?>'),'',sentRaw) # remove tags from sentencs
        posCount = posCount + len(foodList)
        for item in foodList:
            posListOrg.append((docID, item))
        
        # POS tag
        try:
            wordList = nltk.pos_tag(parseSlash(nltk.word_tokenize(sentClean)))
        except:
            print('error:',docID)
            print(sentClean)
            sys.exit(0)
            
        wordList = correctTag(wordList)
        
        # get entities with 1, 2, 3, 4 number of words
        for numword in [1,2,3,4]:
            for idx, x in enumerate(wordList):
                if idx == len(wordList) - (numword-1):
                    break        
                if prune(wordList[idx:(idx+numword)]):    # pruning rules
                    attributes = getAttributes(wordList, foodList, idx, numword);
                    attributes.update({'docID':docID})
                    allEntities.append(attributes)
    
    # compile to relational table    
    data = pd.concat([pd.DataFrame(ent, index = [idx]) for idx,ent in enumerate(allEntities)]) 
    
    # print number of positive entities and total examples
    print(data['label'].value_counts().loc[True], data.shape[0])
    print(posCount)
    
    # identity positive entities that are not extracted
    posList = data[data['label'] == True][['docID','word_0']]
    posListTup = [tuple(x) for x in posList.to_records(index = False)]
    omitted = pd.DataFrame(list(set(posListOrg) - set(posListTup)))
    print(set(posListOrg) - set(posListTup))
    
    # save
    os.chdir('..')
    data.to_csv('set_I_examples.csv', index = False)
    
    