import h5py
import ROOT
import numpy as np
import os
import fnmatch
import pandas as pd
import sys

assert len(sys.argv) >= 4, 'Incorret number of arguments'
dataset_dir = sys.argv[1] #use the command line argument as the directory path to extract data
target_path = sys.argv[2] #use the command line argument as the directory path to store filtered data
feature_columns = sys.argv[3:] #use the command line argument as columns that we want to extract

files_lst = os.listdir(dataset_dir) #all file names in the given directory
fname_lst = fnmatch.filter(files_lst, '*.h5') #filtered file name list: we only take h5 file

#define sorting function
def sort_bc_jets(file, label, target_path, columns):

    """Store the corresponding jets data to the target file
    parameter:
        file(h5 file): the data file that I want to extract data from
        label(int): the label of jet type that I want to sort
        target_path(string): the name of path where I want to store the sorted data
        colunms(list): the name of columns that want to extract

    return:
        None
    """
    file = h5py.File(dataset_dir + '/' + file, 'r') #open file with h5py
    dataset = file["jets"]
    jet_data = dataset[dataset["HadronConeExclTruthLabelID"]==label][feature_columns] #extract a specific jet data point
    temp_df = pd.DataFrame(jet_data)
    if not os.path.exists(target_path) or os.stat(target_path).st_size ==0: #if there are lsdata in the csv file, avoid import header once again
        temp_df.to_csv(target_path, mode= 'a', index = False)
    else:
        temp_df.to_csv(target_path, mode= 'a', index = False, header = False)
    
label_dict = {5: "/b_jet.csv", 4: "/c_jet.csv"} #store the label and its corresponding storage file
for label in [5,4]:
    result_path = target_path + label_dict[label]
    for file in fname_lst:
        sort_bc_jets(file, label, result_path, feature_columns)
