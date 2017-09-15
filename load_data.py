#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 21:27:29 2017

@author: Derek
"""

import pickle
import os

"""load data from pickle"""

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        f.close()

"""change path to desired directory"""
os.chdir("~/")

H_data = load_obj('H_data')
H_labels = load_obj('H_labels')
P_data = load_obj('P_data')
P_labels = load_obj('P_labels')

