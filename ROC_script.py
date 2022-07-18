"""
    The ROC curve script for c-tagging algorithm.
"""
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

assert len(sys.argv) == 2, 'Incorret number of arguments'
dataset_dir = sys.argv[1] #use the command line argument as the directory path to extract data

b_jet = (pd.read_csv(dataset_dir + '/b_jet.csv')).to_numpy()
c_jet = (pd.read_csv(dataset_dir + '/c_jet.csv')).to_numpy()

#Calculate ATLAS_score(ln(pc/pb))
b_ATLAS = np.log(np.divide(b_jet[:,1], b_jet[:,0]))
c_ATLAS = np.log(np.divide(c_jet[:,1], c_jet[:,0]))

#Calculate CMS_score(pc/(pc+pb))
b_CMS = np.divide(b_jet[:,1], b_jet[:, 0] + b_jet[:, 1])
c_CMS = np.divide(c_jet[:,1], c_jet[:, 0] + c_jet[:, 1])

b_len, c_len = b_jet.shape[0], c_jet.shape[0] #The total number of each jet

#calculate efficiency for two discriminant method
#ATLAS-score
thresh_ATLAS = np.linspace(-5, 4, 100)
b_eff_ATLAS = np.array([np.count_nonzero((b_ATLAS > thresh)) for thresh in thresh_ATLAS])/b_len
c_eff_ATLAS = np.array([np.count_nonzero((c_ATLAS < thresh)) for thresh in thresh_ATLAS])/c_len
b_rej_ATLAS = 1/b_eff_ATLAS
#CMS-score
thresh_CMS = np.linspace(0.05, 0.95, 100)
b_eff_CMS = np.array([np.count_nonzero((b_CMS > thresh)) for thresh in thresh_CMS])/b_len
c_eff_CMS = np.array([np.count_nonzero((c_CMS < thresh)) for thresh in thresh_CMS])/c_len
b_rej_CMS = 1/b_eff_CMS

#plot the ROC curve
plt.figure(figsize=(8,6), dpi=100)
plt.plot(c_eff_ATLAS, b_rej_ATLAS, ".", label = "ATLAS")
plt.yscale("log", base = 10)
plt.xlabel("c-jet efficiency")
plt.ylabel("b-jet rejection")
plt.title("ROC curve for c-tagging baseline discriminant")
plt.plot(c_eff_CMS, c_eff_ATLAS, ".", label = "CMS")
plt.legend()
plt.savefig("ROC_curve.png")
