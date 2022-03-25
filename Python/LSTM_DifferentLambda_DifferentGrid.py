"""
Created on Tue Nov 30 17:39:23 2021

@author: ASUS
"""

from numpy import array
from numpy import argmax

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as Keras

import matplotlib.pyplot as plt
import inspect

list_trajectory = []                        # vetor de listas que contem as trajetorias

n = 8                                 # numero celulas na sequencia
n_window = 1
n_epochs = 1000 
batchsize = 64 ##### 512

n_hidden_units = 16  #### 16
n_outputs = 3 #n_outputs
n_cells = 16
n_features = 1 #constant
file_trajectory = "MUNSTER16.txt" 

def sequences_split():
    X = []
    y = []
    
    l = []
    
    for item in list_trajectory:
        l = [item[i:i + n] for i in range(0, len(item), n_window)]  # divide cada trajetoria em sequencias de n celulas
        l_aux=[]
        
        for seq in l:                                       # percorre cada sequencia que resulta da divisao
            if len(seq) == n:
                for i in range(0, len(seq)): 
                    seq[i] = int(seq[i])  
                    
                seq_x, seq_y = seq[0:n-n_outputs], seq[n-n_outputs:n]
                X.append(seq_x)
                y.append(seq_y)
    
    return array(X), array(y)
    

with open(file_trajectory) as file:

    for line in file:
        line = line.strip()                 #vai ler cada linha do ficheiro munster
        t = line.split(" ")                 # converte a string da linha numa lista

        if len(t) >= n:                     # verifica se a trajectoria tem mais que n celulas
            list_trajectory.append(t)

X, y = sequences_split()

X = X.reshape((X.shape[0], X.shape[1], n_features))

encoded_X = to_categorical(X, num_classes=n_cells+1)
encoded_y = to_categorical(y, num_classes=n_cells+1)

teste_encoded_y = encoded_y.reshape((encoded_y.shape[0], encoded_y.shape[1]*encoded_y.shape[2]))

#print(encoded_X.shape)
#print(encoded_y.shape)

#print(teste_encoded_y.shape)
#print(teste_encoded_y)
#print(encoded[1][2])
#print(encoded_y[1][1])





# define model
model = tf.keras.Sequential()
model.add(LSTM(n_hidden_units, activation='tanh', input_shape=(n-n_outputs, n_cells+1),return_sequences=False)) #### tanh
model.add(Dense(n_outputs*(n_cells+1), activation='sigmoid'))
model.compile(optimizer='adam', loss='categorical_crossentropy')

# fit model
checkLoss = model.fit(encoded_X, teste_encoded_y, epochs=n_epochs, batch_size=batchsize, verbose=2)


#print(inspect.getmembers(checkLoss))


plt.plot(checkLoss.history['loss'])
plt.xlabel('Epochs ')
plt.ylabel('Loss')
plt.show()

model.save(f'my_model_Lambda{n}_outputs{n_outputs}_N{n_cells}.h5')  # creates a HDF5 file 'my_model.h5'