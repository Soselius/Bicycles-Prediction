# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:40:52 2022

@author: ASUS
"""

import pickle
import numpy as np
import time
import scipy.io

import tensorflow as tf 
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical



n = 12
n_outputs = 4 
n_cells = 256
n_features = 1
n_window = 1

start_p = pickle.load(open(f'initial_prob.pkl', 'rb'))
sorted_seq = pickle.load(open(f'sorted_Seq.pkl', 'rb'))

model = load_model(f'ANN_Lambda{n}_outputs{n_outputs}_N{n_cells}.h5')


stats_dict = {'total':0, 'correct':0}
prediction_perSeq = []
output1_perSeq = []
output2_perSeq = []
output3_perSeq = []
output4_perSeq = []
output5_perSeq = []
prob_start = []

##########################################################################
def convert_sequence(seq):
    obs_seq = []
    new_seq = [seq[i:i + 3] for i in range(0, len(seq), 3)]
    for item in new_seq:
        if item[0:2] == '00':
            obs_seq.append(item[2])
        elif item[0]=='0':
            obs_seq.append(item[1]+item[2])
        else:
            obs_seq.append(item)

    return obs_seq


#################################################################################################
def statistics(obs, pred_cells):

    control = 1
    output1 = 1
    output2 = 1
    output3 = 1
    output4 = 1
    output5 = 1

    stats_dict['total'] += 1

    for i in range(0, n_outputs):
        
        if i+1 == 1 and int(obs[i]) != int(pred_cells[i]):
            output1 = 0
            control = 0

        if i + 1 == 2 and int(obs[i]) != int(pred_cells[i]):
            output2 = 0
            control = 0

        if i+1 == 3 and int(obs[i]) != int(pred_cells[i]):
            output3 = 0
            control = 0

        if i+1 == 4 and int(obs[i]) != int(pred_cells[i]):
            output4 = 0
            control = 0

        if i+1 == 5 and int(obs[i]) != int(pred_cells[i]):
            output5 = 0
            control = 0

    if control == 1:
        stats_dict['correct'] += 1

    return control, output1, output2, output3, output4, output5

#########################################################################


iter=0
result = 0

for seq in sorted_seq:
    iter=iter+1
    #print(f"Iter {iter}")

    prob_start.append(start_p[seq])
    
    cells_seq = convert_sequence(seq)   # convert sequences into cells
    print(cells_seq)
                    
    seq_x, seq_y = cells_seq[0:n-n_outputs], cells_seq[n-n_outputs:n]
    x_input = np.array(seq_x)
    x_input = x_input.reshape((1, n-n_outputs, n_features))
    encoded_X = to_categorical(x_input, num_classes=n_cells+1)
    
    encoded_X_aux = encoded_X.reshape((encoded_X.shape[0], encoded_X.shape[1]*encoded_X.shape[2])) #add this to have the same dimension
    
    yhat = model.predict(encoded_X_aux)
 
    y_predicted = np.round(np.array(yhat)*1000000000000,0)
    r_y_predicted = y_predicted.reshape((1,n_outputs, n_cells+1))
    
    y_final = np.argmax(r_y_predicted, axis=2)
    y_final = np.array(y_final[0])
    
    corr_cells = np.array(seq_y)
    
    
    [value_estimation, output1, output2, output3, output4, output5] = statistics(corr_cells, y_final)

    prediction_perSeq.append(value_estimation)
    output1_perSeq.append(output1)
    output2_perSeq.append(output2)
    output3_perSeq.append(output3)
    output4_perSeq.append(output4)
    output5_perSeq.append(output5)


       
scipy.io.savemat(f'Prediction_onehot_ANN_L{n}_o{n_window}_outputs{n_outputs}_N{n_cells}.mat', {f'Prediction_onehot_ANN_L{n}_o{n_window}_outputs{n_outputs}_N{n_cells}': [prob_start, prediction_perSeq, output1_perSeq, output2_perSeq, output3_perSeq, output4_perSeq, output5_perSeq]})







