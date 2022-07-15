import numpy as np

def cross_entropy_cost(Y_hat, Y):
    m = Y.shape[1]
    logprobs = np.dot(np.log(Y_hat), Y.T)+ np.dot(np.log(1-Y_hat),(1-Y).T)
    cost = np.divide(logprobs, -m)
    cost = float(np.squeeze(cost))
    return cost

def logistic_cost(Y_hat, Y):
    m = Y.shape[1]
    loss = np.dot(Y, np.log(Y_hat).T) + np.dot((1-Y),np.log(1-Y_hat).T)
    cost = np.divide(loss, -m)
    print(cost)
    cost = float(np.squeeze(cost))
    
    return cost

def mean_squared_error(Y_hat, Y):
    m = Y.shape[1]
    diff = Y-Y_hat
    loss = np.dot(diff, diff)
    cost = np.divide(loss, 2*m)
    cost = float(np.squeeze(cost))
    return cost