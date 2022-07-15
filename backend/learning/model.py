import numpy as np
import numpy as np
from backend.learning.activation.activation import sigmoid
from backend.learning.loss.cost import cross_entropy_cost
import pandas as pd

class OneHiddenLayerModel:

    def __init__(self, parameters={}):
        self.parameters = parameters
        self.costs = []
        self.cumulative_gradient = {"dW1": 0,
                    "db1": 0,
                    "dW2": 0,
                    "db2": 0}

    def initialize_parameters(self, n_x, n_h, n_y):
        """
        Argument:
        n_x -- size of the input layer
        n_h -- size of the hidden layer
        n_y -- size of the output layer
        
        Returns:
        params -- python dictionary containing your parameters:
                        W1 -- weight matrix of shape (n_h, n_x)
                        b1 -- bias vector of shape (n_h, 1)
                        W2 -- weight matrix of shape (n_y, n_h)
                        b2 -- bias vector of shape (n_y, 1)
        """ 
        #np.random.seed(2)   
        W1 = np.random.randn(n_h,n_x) * 0.01
        b1 = np.zeros((n_h,1))
        W2 = np.random.randn(n_y,n_h) * 0.01
        b2 = np.zeros((n_y,1))

        parameters = {"W1": W1,
                    "b1": b1,
                    "W2": W2,
                    "b2": b2}
        return parameters

    def forward_propagation(self, X):
        """
        Argument:
        X -- input data of size (n_x, m)
        parameters -- python dictionary containing your parameters (output of initialization function)
        
        Returns:
        A2 -- The sigmoid output of the second activation
        cache -- a dictionary containing "Z1", "A1", "Z2" and "A2"
        """
        parameters = self.parameters
        W1 = parameters['W1']
        b1 = parameters['b1']
        W2 = parameters['W2']
        b2 = parameters['b2']

        # define layers and activations
        Z1 = np.dot(W1, X) + b1
        A1 = np.tanh(Z1) # tanh used in activation of hidden layer
        Z2 = np.dot(W2, A1) + b2
        A2 = sigmoid(Z2) # Y_pred
        
        assert A2.shape == (1, X.shape[1]), "shape of matrices doesn't match"
        
        cache = {"Z1": Z1,
                "A1": A1,
                "Z2": Z2,
                "A2": A2}
        
        return A2, cache
    
    def backward_propagation(self, cache, X, Y):
        """
        Arguments:
        parameters -- python dictionary containing our parameters 
        cache -- a dictionary containing "Z1", "A1", "Z2" and "A2".
        X -- input data of shape (2, number of examples)
        Y -- "true" labels vector of shape (1, number of examples)
        
        Returns:
        grads -- python dictionary containing your gradients with respect to different parameters
        """
        m = X.shape[1]
        parameters = self.parameters
        W1 = parameters['W1']
        W2 = parameters['W2']
        A1 = cache['A1']
        A2 = cache['A2']

        dZ2 = A2-Y
        dW2 = np.divide(np.dot(dZ2, A1.T), m)
        db2 = np.divide(np.sum(dZ2, axis=1, keepdims=True), m)
        dZ1 = np.multiply(np.dot(W2.T,dZ2), (1-np.power(A1,2))) ## not dW2.T
        dW1 = np.divide(np.dot(dZ1, X.T), m)
        db1 = np.divide(np.sum(dZ1, axis=1, keepdims=True), m)
        
        grads = {"dW1": dW1,
                "db1": db1,
                "dW2": dW2,
                "db2": db2}
        
        return grads
    
    def gradient_descent_step(self, grads, learning_rate = 0.01):
        """
        Updates parameters using the gradient descent update rule given above
        
        Arguments:
        parameters -- python dictionary containing your parameters 
        grads -- python dictionary containing your gradients 
        
        Returns:
        parameters -- python dictionary containing your updated parameters 
        """
        # Retrieve weights and biases
        parameters = self.parameters
        W1 = parameters['W1']
        b1 = parameters['b1']
        W2 = parameters['W2']
        b2 = parameters['b2']
        
        # Retrieve gradients
        dW1 = grads['dW1']
        db1 = grads['db1']
        dW2 = grads['dW2']
        db2 = grads['db2']

        # Update rule for each parameter
        W1 = W1 - learning_rate * dW1
        b1 = b1 - learning_rate * db1
        W2 = W2 - learning_rate * dW2
        b2 = b2 - learning_rate * db2

        # update dictionary-parameters
        self.parameters = {"W1": W1,
                    "b1": b1,
                    "W2": W2,
                    "b2": b2}
    
    def train_nn_model(self, X, Y, n_hidden, num_iterations=1, learning_rate=0.01, batch_size=False, print_cost=False):
        """
        Arguments:
        X -- Input vector
        Y -- labels
        n_hidden: hidden layer size
        """
        n_x = X.shape[0]
        n_y = Y.shape[0]
        m_x = X.shape[1]
        self.parameters = self.initialize_parameters(n_x, n_hidden, n_y)
        costs = []
        self.trained_examples = set()
        for i in range(num_iterations):
            Y_batch = None
            if batch_size: # if batch_size is set mini batches will be used to optimize
                batch = np.random.choice(range(m_x), batch_size)
                self.trained_examples.update(batch)
                X_batch = X[:,batch]
                Y_batch = Y[0,batch].reshape(1,-1)
                A2, cache = self.forward_propagation(X_batch)
                grads = self.backward_propagation(cache, X_batch, Y_batch)
                
                self.cumulative_gradient = {k: np.add(self.cumulative_gradient[k], grads[k]).tolist() for k in self.cumulative_gradient.keys()}
                #print(f'grads: {grads}, cumulative_gradient: {self.cumulative_gradient}')
            else:
                A2, cache = self.forward_propagation(X)
                grads = self.backward_propagation(cache, X, Y)

            # update parameters
            self.gradient_descent_step(grads,learning_rate=learning_rate)

            if print_cost and i % 10 == 0:
                if batch_size:
                    cost = cross_entropy_cost(A2, Y_batch)
                else:
                    cost = cross_entropy_cost(A2, Y)

                costs.append(cost)
                print("Cost after iteration %i: %f" %(i, cost))
        self.cumulative_gradient = {k: np.squeeze(np.divide(self.cumulative_gradient.get(k),num_iterations)).tolist() for k in self.cumulative_gradient.keys()}
        self.costs = costs
        return self.parameters