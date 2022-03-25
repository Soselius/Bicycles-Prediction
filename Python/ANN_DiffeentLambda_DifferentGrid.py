# -*- coding: utf-8 -*-


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

#print(X[1:3])
X = X.reshape(X.shape[0], X.shape[1])


#print(X[1:15])

encoded_X = to_categorical(X, num_classes=n_cells+1)

encoded_X_aux = encoded_X.reshape((encoded_X.shape[0], encoded_X.shape[1]*encoded_X.shape[2]))


encoded_y = to_categorical(y, num_classes=n_cells+1)

#print(encoded_X_aux[1:3])
#print(encoded_y[1:3])
#print(encoded_y[1:3])

teste_encoded_y = encoded_y.reshape((encoded_y.shape[0], encoded_y.shape[1]*encoded_y.shape[2]))
#print(teste_encoded_y[1:3])

#print(encoded_X.shape)
#print(encoded_y.shape)

#print(teste_encoded_y.shape)
#print(teste_encoded_y)
#print(encoded[1][2])
#print(encoded_y[1][1])





# define model ANN
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense((n-n_outputs)*(n_cells+1), input_dim = (n-n_outputs)*(n_cells+1), activation = 'relu')) #### tanh
model.add(Dense((n-n_outputs) * 0.8 *(n_cells+1), activation='relu'))
model.add(Dense((n-n_outputs) * 0.6 *(n_cells+1), activation='relu'))
model.add(Dense(n_outputs*(n_cells+1), activation='softmax'))
callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10)
model.compile(optimizer='adam', loss='mean_squared_error')

# fit model
checkLoss = model.fit(encoded_X_aux, teste_encoded_y, epochs=n_epochs, batch_size=batchsize, verbose=2, callbacks=[callback])


#print(inspect.getmembers(checkLoss))


plt.plot(checkLoss.history['loss'])
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()

model.save(f'ANN_Lambda{n}_outputs{n_outputs}_N{n_cells}.h5')  # creates a HDF5 file 'my_model.h5'


# model = Sequential()
# model.add(Dense(num_inputs*2, input_dim=num_inputs*2, activation='relu'))
# model.add(Dense(8, activation='relu'))
# model.add(Dense(4, activation='softmax'))

# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# ## run the training stage ........
# history = model.fit(x_train, y_train,validation_data = (x_test,y_test), epochs=100, batch_size=64, callbacks=[callback])