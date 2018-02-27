#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 15:48:41 2018

@author: kangyanghui
"""

from shutil import copyfile
import csv

with open('doc_split.csv') as docListFile:
    csvReader = csv.reader(docListFile)
    for row in csvReader:
        print(row)
        if row[2] == '1':
            copyfile('markup_v2/all/'+row[0]+'.txt','markup_v2/set_I/'+row[0]+'.txt')
        if row[2] == '0':
            copyfile('markup_v2/all/'+row[0]+'.txt','markup_v2/set_J/'+row[0]+'.txt')

