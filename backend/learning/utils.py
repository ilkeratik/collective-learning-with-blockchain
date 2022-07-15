from operator import ne
import numpy as np
import pandas as pd
import uuid, time
from backend.blockchain.model_block import ModelBlock

from backend.learning.model import OneHiddenLayerModel 
from backend.message.train_msg import TrainMessage
from backend.message.validation_msg import ValidationMessage
from backend.message.task_msg import TaskMessage
from backend.message.model_msg import ModelMessage


def create_block(wallet, blockchain, TrainMessage, TaskMessage, validation_pool):
    """
    Create a block.
    """
    miner = wallet.address
    task_id = TrainMessage.task_id
    trainer = TrainMessage.trainer_address
    agg_res = aggregate_and_compare_results(TrainMessage, validation_pool)
    validators = agg_res['validators']
    grad_vector = agg_res['gradient_vector']
    source = agg_res['source']
    loss = agg_res['loss']
    curr_parameters = TaskMessage.model.parameters
    curr_difficulty = TaskMessage.min_validator
    new_parameters = model_update(curr_parameters, grad_vector)

    block_data= {
        'task_id': task_id,
        'contributors': {'trainer': trainer, 
                        'validators': validators, 
                        'miner': miner},

        'model_update': {'source': source, 
                        'gradient_vector': {k: grad_vector[k].tolist() for k in grad_vector.keys()}, 
                        'parameters': {k: new_parameters[k].tolist() for k in new_parameters.keys()}, 
                        'metrics': {'loss': loss}
                        },
    }
    

    return block_data

def model_update(parameters, gradient_vector, learning_rate = 0.1):
    """
    Model update using gradient.
   
    Updates parameters using the gradient descent update rule given above
    
    Arguments:
    parameters -- python dictionary containing your parameters 
    grads -- python dictionary containing your gradients 
    
    Returns:
    parameters -- python dictionary containing your updated parameters 
    """
    
    # Retrieve weights and biases
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    
    # Retrieve gradients
    dW1 = gradient_vector['dW1']
    db1 = gradient_vector['db1']
    dW2 = gradient_vector['dW2']
    db2 = gradient_vector['db2']

    # Update rule for each parameter
    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2

    # update dictionary-parameters
    parameters = {"W1": W1,
                "b1": b1,
                "W2": W2,
                "b2": b2}
    return parameters

def training(wallet, task_msg):
    """
    Training function.
    """
    
    model = OneHiddenLayerModel()
    data_path = task_msg.model.data_path
    df = pd.read_csv(data_path)
    (X, Y) = df.iloc[:,:-1].values, df.iloc[:,-1].values
    model.train_nn_model(X.T, Y.reshape((-1,1)).T, 5, num_iterations=300, learning_rate=0.01, batch_size=32, print_cost=True)
    examples_list = list(map(int,model.trained_examples))
    latest_loss = model.costs[-1]
    metrics = {
        'loss': latest_loss
    }
    gradient_vector = model.cumulative_gradient
    #print(f'shape train{gradient_vector.shape}')
    task_id = task_msg.id
    trainer_address = wallet.address
    public_key = wallet.public_key

    id = str(uuid.uuid4())[0:8]
    timestamp = time.time_ns()
    bet_amount = 32
    train_msg = TrainMessage.from_dict({'id':id
                                        ,'timestamp':timestamp
                                        ,'public_key':public_key
                                        ,'task_id':task_id
                                        ,'trainer_address':trainer_address  
                                        ,'examples_list':examples_list
                                        ,'gradient_vector':gradient_vector
                                        ,'metrics':metrics
                                        ,'bet_amount':bet_amount })
    
    return train_msg

def validation(wallet, TaskMessage, TrainMessage):
    """
    Validation function.
    """
    
    model = OneHiddenLayerModel()
    data_path = TaskMessage.model.data_path

    df = pd.read_csv(data_path)
    (X, Y) = df.iloc[:,:-1].values, df.iloc[:,-1].values
    (X,Y) = X[TrainMessage.examples_list], Y[TrainMessage.examples_list]
    model.train_nn_model(X.T, Y.reshape((-1,1)).T, 5, num_iterations=30, learning_rate=0.01, batch_size=1, print_cost=True)
    
    sub_trained_examples = list(map(int,model.trained_examples))
    latest_loss = model.costs[-1]
    metrics = {
        'loss': latest_loss
    }
    gradient_vector = model.cumulative_gradient
    #print(f'shape valid{gradient_vector.shape}')
    train_id = TrainMessage.id
    validator_address = wallet.address
    public_key = wallet.public_key
    
    id = str(uuid.uuid4())[0:8]
    timestamp = time.time_ns()
    bet_amount = 32
    validation_msg = ValidationMessage.from_dict({'id':id
                                        ,'timestamp':timestamp
                                        ,'public_key':public_key
                                        ,'train_id':train_id
                                        ,'validator_address':validator_address  
                                        ,'sub_trained_examples':sub_trained_examples
                                        ,'gradient_vector':gradient_vector
                                        ,'metrics':metrics
                                        ,'bet_amount':bet_amount })
    
    return validation_msg

def aggregate_and_compare_results(TrainMessage, validation_pool):
    """
    Aggregate and compare results.
    """
    
    validators = []
    validation_gradient_vectors = []
    validation_losses = []
    for elem in validation_pool:
        validators.append(elem['data']['validator_address'])
        validation_gradient_vectors.append(elem['data']['gradient_vector'])
        validation_losses.append(elem['data']['metrics']['loss'])
    # Aggregate losses
    validation_losses_average = np.mean(validation_losses)
    # Aggregate the gradient vectors
    dw1 = list(map(lambda grd: grd['dW1'], validation_gradient_vectors))
    db1 = list(map(lambda grd: grd['db1'], validation_gradient_vectors))
    dw2 = list(map(lambda grd: grd['dW2'], validation_gradient_vectors))
    db2 = list(map(lambda grd: grd['db2'], validation_gradient_vectors))

    dw1_avg = np.squeeze(np.mean(dw1, axis=0, keepdims=True))
    db1_avg = np.squeeze(np.mean(db1, axis=0, keepdims=True))
    dw2_avg = np.squeeze(np.mean(dw2, axis=0, keepdims=True))
    db2_avg = db2[0]
    val_gradient_vector_avg = {'dW1': dw1_avg, 'db1': db1_avg, 'dW2': dw2_avg, 'db2': db2_avg}
    
    # dw1_std = np.std(dw1, axis=0)
    # db1_std = np.std(db1, axis=0)
    # dw2_std = np.std(dw2, axis=0)
    # db2_std = np.std(db2, axis=0)
    # val_gradient_vector_std = list([dw1_std, db1_std, dw2_std, db2_std])
    # val_gradient_vector_std = np.sum(val_gradient_vector_std, axis=1)
    # print(f'val_gradient_vector_std: {val_gradient_vector_std}')
    #validation_gradient_vector_average = list(map(lambda grd: np.mean(grd), validation_gradient_vectors))
    
    # Calculate standard deviation of the gradient vectors
    #validation_gradient_vector_std = np.std(validation_gradient_vectors, axis=0)

    train_gradient_vector = TrainMessage.gradient_vector
    # for key in train_gradient_vector.keys():
    #     print(f'train_gradient_vector: {train_gradient_vector[key]} \n val_gradient_vector_avg: {val_gradient_vector_avg[key]}')
    train_loss = TrainMessage.metrics['loss']
    is_similar = likelihood_function(train_gradient_vector, train_loss, val_gradient_vector_avg, validation_losses_average)

    if is_similar:
        aggregated_vector = dict()
        for key in train_gradient_vector.keys():
            # print(f'train_gradient_vector: {train_gradient_vector[key]} \n val_gradient_vector_avg: {val_gradient_vector_avg[key]}')
            aggregated_vector[key] = np.multiply(0.1,val_gradient_vector_avg[key]) + np.multiply(0.9,train_gradient_vector[key]).tolist()
        return {
            'validators': validators,
            'source': "aggregated",
            'gradient_vector': aggregated_vector,
            'loss':{'train': train_loss, 
                    'validation': validation_losses_average}
        }
    else:
        return {
            'validators': validators,
            'source': "only_validation",
            'gradient_vector': val_gradient_vector_avg,
            'loss':{'train': train_loss, 
                    'validation': validation_losses_average}
        }



def likelihood_function(train_gradient, train_loss, valid_gradient, validation_loss_avg):
    """
    Likelihood function.
    """
    diff = 0
    for key in train_gradient.keys():
            diff +=  np.sum(np.abs(train_gradient[key] - valid_gradient[key]))
    diff_loss = 1e2*(train_loss - validation_loss_avg)
    diff_sum = diff
    print(f'Difference: {diff_sum}, Loss diff: {diff_loss}')
    if diff_loss+diff_sum< 1e4:
        return True
    else:
        return False
    
def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<m]
if __name__ == '__main__':
    msg = TrainMessage.from_dict({'id':31
                                        ,'timestamp':1212
                                        ,'public_key':424242
                                        ,'task_id':1212
                                        ,'trainer_address':555
                                        ,'examples_list':[]
                                        ,'gradient_vector':[3,4,5]
                                        ,'metrics':{'loss': 0.08}
                                        ,'bet_amount':32 })
    train_id = msg.id
    model_msg = ModelMessage.from_dict({'id':322
                                    , 'name': 'OneHiddenLayerModel'
                                    , 'description': 'Test One hidden layer model to train fraud data'
                                    , 'data_path': 'backend\learning\datasets\fraud_detection\mini_ds_creditcard.csv'
                                    , 'parameters': {"W1": [0.2,0.23,0.11],
                                                    "b1": [0],
                                                    "W2": [0.1,0.2,0.3],
                                                    "b2": [1]}
                                    , 'latest_gradient': [0.1,0.2,0.3]
                                    , 'current_metrics': {'loss': 0.4}
                                    ,'contributors': ['ilker_aa']
    })
    
    task_msg = TaskMessage.from_dict({'id':31
                                ,'timestamp':1212
                                ,'public_key':424242
                                ,'owner_address': 'ilker_aa'
                                ,'model': model_msg
                                ,'min_validator': 2
                                ,'evaluation_metrics': ['loss']
    })

    data_path = task_msg.model.data_path
    losss = task_msg.model.current_metrics['loss']
    task_msg.model.parameters['W1'] = [0.31,0.31]
    print(task_msg.model.parameters)