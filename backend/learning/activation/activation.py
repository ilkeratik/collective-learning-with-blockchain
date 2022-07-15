import numpy as np

def sigmoid(x):
    s = 1/(1+np.exp(-x))
    return s

def sigmoid_derivative(x):
    s = sigmoid(x)
    ds = s*(1-s)
    return ds

def relu(x):
    return np.maximum(0, x)

def leaky_relu(x):
    return np.maximum(0.01*x,x)

def tanh(x):
    """
    It returns the value (1-exp(-2x))/(1+exp(-2x)) and the value
    returned will be lie in between -1 to 1.
    """
    return np.tanh(x)

def tanh_derivative(x):
    t = tanh(x)
    dt=1-t**2
    return dt