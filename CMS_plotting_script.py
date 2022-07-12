import h5py
import ROOT
import numpy as np
import os
import pandas as pd
import sys

#use the command line argument as the name that you want to store the diagram
assert len(sys.argv) == 2, 'Incorret number of arguments'
hist_name = sys.argv[1]

#extracting data from b_jet and c_jet file
b_jet = pd.read_csv('b_jet.csv', usecols = ['DL1r_pb', 'DL1r_pc']) #only extract these two columns
c_jet = pd.read_csv('c_jet.csv', usecols = ['DL1r_pb', 'DL1r_pc'])


#compute the discriminant score for each data point
np_b_jet = b_jet.to_numpy()
bjet_CMS = np.divide(np_b_jet[:,1], np_b_jet[:,0]+np_b_jet[:,1]) #CMS-like discriminant score for all b-jet
np_c_jet = c_jet.to_numpy()
cjet_CMS = np.divide(np_c_jet[:,1], np_c_jet[:,0]+np_c_jet[:,1]) #CMS-like discriminant score for all c-jet


#Draw a ROOT histogram to show the discriminant distribution
b_CMS_plot = ROOT.TH1D("b-jet","CMS-like distribution",20,0,25)
c_CMS_plot = ROOT.TH1D("c-jet","CMS-like distribution",20,0,25)

b_CMS_plot.SetLineColor(2)
c_CMS_plot.SetLineColor(3)

b_len, c_len = bjet_CMS.shape[0], cjet_CMS.shape[0]

b_CMS_plot.FillN(b_len, bjet_CMS, 1/b_len*np.ones(b_len))
c_CMS_plot.FillN(c_len, cjet_CMS, 1/c_len*np.ones(c_len))

stack = ROOT.THStack("stack", "CMS-like score(pc/(pc+pb)) distribution for b- and c-jet")
stack.Add(b_CMS_plot)
stack.Add(c_CMS_plot)
c = ROOT.TCanvas("myCanvasName","The Canvas Title",800,600)
stack.Draw("nostack")
stack.GetYaxis().SetTitle("portion of events")
stack.GetXaxis().SetTitle("pc/pb score")
c.Draw()
legend = ROOT.TLegend(0.7, 0.7 ,0.82 ,0.82)
legend.AddEntry(b_CMS_plot, "b-jet")
legend.AddEntry(c_CMS_plot, "c-jet")
legend.Draw()
c.SaveAs(hist_name + '.png')