import numpy as np
import pandas as pd

#Copy and pasted script from old coursework

#Define hyperparameters for the model
epochs = 100
batchSize = 1 #Batch Size, 1 is SGD, N (size of dataset) is GD, M where 1<M<N is Batch GD
learningRate = 1e-4

def read_data(path):
    df = pd.read_csv(path)
    dT = df['dT[C]'].to_numpy().reshape(-1,1)
    Qdot = df['Qdot[W]'].to_numpy().reshape(-1,1)
    return dT, Qdot


def SGD(dT, Qdot, weight, bias, epochs, batchSize, learningRate):# Training Loop

    steps = int(dT.shape[0]/batchSize) #Number of steps required for an epoch
    weight_init = float(weight)
    bias_init = float(bias)

    for i in range(epochs):
        
        for n in range(steps):
            
            #Index array of randomly picked indexes of the training samples to choose elements in the batch
            index = np.random.choice(np.arange(dT.shape[0]),batchSize,replace=True)
            
            #Use index to create an array for the batches of the training data
            dT_batch = dT[index,:]
            Qdot_batch = Qdot[index,:]
            
            #Forward pass to calculate mean squared error
            MSE = (1/batchSize) * np.sum((Qdot_batch - (weight*dT_batch + bias))**2,axis=0)
            
            #Backward pass takes the sum over axis 0 to implement batch gradient descent
            dWeight = (1/batchSize) * np.sum(-2.0 * dT_batch * (Qdot_batch - (weight*dT_batch + bias)),axis=0)
            dBias = (1/batchSize) * np.sum(-2.0 * (Qdot_batch - (weight*dT_batch + bias)),axis=0)

            #Bug += instead of -=
            weight += learningRate*dWeight
            bias +=  learningRate*dBias


            #Calculate loss over entire training dataset
            MSE_epoch = (1/dT.shape[0]) * np.sum((Qdot - (weight*dT + bias))**2,axis=0)
            breakpoint()
            
    return weight, bias

def main():

    dT, Qdot = read_data('window_heat.csv')

    #Initialize weight array as a gaussian N(0,1) and initialize bias array as zeros
    weight_init = np.random.randn(dT.shape[1])
    bias_init = np.zeros(dT.shape[1])

    # Training Loop

    weight, bias = SGD(dT, Qdot, weight_init, bias_init, epochs, batchSize, learningRate)
            
            
    print(weight, bias)

main()