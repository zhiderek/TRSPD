# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 14:13:36 2017
Load the joint positions and the labels from csv files and store them in pickle
@author: zhid

"""
import numpy as np
import os
import pickle
from pdb import set_trace

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        f.close()
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

#rootdir = '~\directory_where_files_are_located'
rootdir = '/Users/Derek/Desktop/db_final/data/'
os.chdir(rootdir + 'data_new')
subjects = [name for name in os.listdir(".") if os.path.isdir(name)]

joints_sel = range(1,26) #select the desired joint numbers. ref: https://msdn.microsoft.com/en-us/library/microsoft.kinect.jointtype.aspx
total_joint_num = 25
invert_data = True

HsubNames = []
Hlbl_set  = []
Hdata_set = []

PsubNames = []
Plbl_set  = []
Pdata_set = []

for sub in subjects:
    print '==========================='+sub+'============================'
    os.chdir(rootdir+'data_new'+'/'+sub)
    tasks = [name for name in os.listdir('.') if os.path.isdir(name)]
    lbl = np.empty([0,1])
    data = np.empty([0,3*len(joints_sel)])
    
    """ Load data and labels"""
    for task in tasks:
        print task
        fname = rootdir + 'data_new/' + sub + '/'+ task+'/'+'Joint_Positions.csv'
        if os.path.isfile(fname):
            print 'loading '+ task + ' '
            data_loaded = np.loadtxt(open(fname),delimiter=",")
            frame_num = len(data_loaded)/total_joint_num
            features = np.empty((frame_num, 3*len(joints_sel)))
            for index, row in enumerate(data_loaded):
                f = index // total_joint_num
                r = index % total_joint_num
                if r in joints_sel:
                    """ x: flip the joinst if necessary """
                    if invert_data and 'L' in task:
                        features[f, joints_sel.index(r)] = -row[0]
                    else:
                        features[f, joints_sel.index(r)] = row[0]
                    """ z """
                    features[f, joints_sel.index(r) + len(joints_sel)] = row[1]
                    """ y """
                    features[f, joints_sel.index(r) + 2 * len(joints_sel)] = row[2]
        else:
            print task + ' doesn\'t exist'
        #=================load labels ===================================
        fname = rootdir + 'data_new/' + sub + '/' + task + '/' + 'Labels.csv'
        if os.path.isfile(fname):
            print 'loading ' + task + ' labels'
            labels = np.loadtxt(open(fname), delimiter = ",")
            if len(labels) != len(features):
                "lengths don't match"
                set_trace()
        data = np.concatenate((data,features),axis=0)
        lbl = np.concatenate((lbl, labels.reshape(-1,1)), axis = 0)
        
    """ Assign data and labels to healthy or patients"""
    if sub[0] == 'H':
        HsubNames.append(sub)
        Hdata_set.append(data)
        Hlbl_set.append(lbl)
    elif sub[0] == 'P':
        PsubNames.append(sub)
        Pdata_set.append(data)
        Plbl_set.append(lbl)

H_data = np.vstack(Hdata_set)
H_labels = np.vstack(Hlbl_set)
H_sub = []
for ii, lbl in enumerate(Hlbl_set):
    H_sub.extend([HsubNames[ii]*lbl.shape[0]])
H_sub_ids = np.stack(H_sub)

P_data = np.vstack(Pdata_set)
P_labels = np.vstack(Plbl_set)
P_sub = []
for ii, lbl in enumerate(Plbl_set):
    P_sub.extend([PsubNames[ii]]*lbl.shape[0])
P_sub_ids = np.stack(P_sub)

"""save to dir"""

os.chdir(rootdir + 'data_new')
save_obj(H_data,"H_data")#only using left hand
save_obj(H_labels,"H_labels")#only using left hand
save_obj(H_sub_ids,"H_sub_ids")#participant number
save_obj(P_data,"P_data")#only using left hand
save_obj(P_labels,"P_labels")#only using left hand
save_obj(P_sub_ids,"P_sub_ids")#participant number
