import numpy as np
def absolute_error(Y_hat, Y):
    """
    Computes absolute error for given prediction and real value matrices.

    Arguments:
    Y_hat -- vector of size m (predicted labels)
    Y -- vector of size m (true labels)
    
    Returns:
    loss -- absolute error
    """
    loss = np.sum(np.abs(Y-Y_hat))
    return loss

def squared_error(Y_hat, Y):
    """
    Arguments:
    Y_hat -- vector of size m (predicted labels)
    Y -- vector of size m (true labels)
    
    Returns:
    loss -- squared error
    """   
    diff = Y-Y_hat
    loss = np.dot(diff, diff)
    return loss

def logistic_loss(Y_hat, Y):
    loss = (Y*np.log(Y_hat)+(1-Y)*np.log(1-Y_hat))
    return loss

def cross_entropy_loss(Y_hat, Y):
    logprobs = np.add(np.multiply(np.log(Y_hat),Y), np.multiply((1-Y),np.log(1-Y_hat)))
    return logprobs