# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 14:13:36 2017

@author: Ying Xuan (Derek) Zhi

This script loads the joint positions and labels 

Modified on July 20 to invert the x coordinate
"""
import numpy as np
import os
from pdb import set_trace
import pickle


""" Data is stored in pickle format for later access"""
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        f.close()

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


""" Set the root dir to where the data folder is"""
rootdir = r"/Users/Derek/Desktop/db_final/db/zip/data"
subjects = [name for name in os.listdir(rootdir) if os.path.isdir(rootdir+"/"+name)]


""" Select joints. 
Ref: https://msdn.microsoft.com/en-us/library/microsoft.kinect.jointtype.aspx"""
joints_sel = range(25)#remove spine base, hips and added head
total_joint_num = 25


""" this flag dictates the inversion of x-axis, used to make both the left and right arm on the one side"""
invert_data = True 


HsubNames = []
Hlbl_set = []
Hdata_set = []

PsubNames = []
Plbl_set = []
Pdata_set = []

for sub in subjects:
    print '==========================='+sub+'============================'
    tasks = [name for name in os.listdir(rootdir+'/'+sub) if os.path.isdir(rootdir+'/'+sub+'/'+name)]
    lbl = np.empty([0,1])
    data = np.empty([0,3*len(joints_sel)])
    
    """ Load data and labels"""
    
    for task in tasks:
        print task
        fname = rootdir + '/' + sub + '/'+ task+'/'+'Joint_Positions.csv'
        if os.path.isfile(fname):
            print 'loading '+ task + ' '
            data_loaded = np.loadtxt(open(fname),delimiter=",")
            frame_num = len(data_loaded)/total_joint_num
            
            
            """ Load features"""
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
        
        
        
        """ Load labels"""
        fname = rootdir + '/' + sub + '/' + task + '/' + 'Labels.csv'
        if os.path.isfile(fname):
            print 'loading ' + task + 'labels'
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


""" Designate dir to store data"""
os.chdir(None)#replace None with your designate path)

""" store data """     
save_obj(Hdata_set,"H_data")
save_obj(Hlbl_set,"H_label")
save_obj(HsubNames,"Hsub")
save_obj(Pdata_set,"P_data")
save_obj(Plbl_set,"P_labels")
save_obj(PsubNames,"Psub")
