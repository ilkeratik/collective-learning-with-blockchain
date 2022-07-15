import random
import requests
import argparse
from backend.app.blockchain_routes import *
from backend.pubsub.pubsub import *
from backend.app.sync_chain_and_pool import *
ROOT_PORT = 5000
PORT = ROOT_PORT

if __name__ == 'backend.app':
    arg_parser = argparse.ArgumentParser(description='CLI args interface for the web app')

    arg_parser.add_argument('-p','--peer', dest='peer', action='store_true',help='Start server as a peer')
    arg_parser.add_argument('-t','--trainer', dest='trainer', action='store_true',help='Start server as a trainer')
    arg_parser.add_argument('-v','--validator', dest='validator', action='store_true',help='Start server as a validator')
    arg_parser.add_argument('-m','--miner', dest='miner', action='store_true',help='Start server as a miner')

    arg_parser.set_defaults(peer=False, trainer=False)

    args = arg_parser.parse_args()

    if args.peer:
        print("Started server as peer")
        PORT = random.randint(5001, 6000)
        sync_blockchain(blockchain)
        sync_transaction_pool(transaction_pool)
        
    elif args.trainer:
        print("Started server as trainer")
        PORT = random.randint(5001, 6000)
        print(PORT)
        pubsub = TrainerPubSub(model_blockchain, task_pool, train_pool)
        sync_model_blockchain(model_blockchain)
        sync_task_pool(task_pool)
        
    elif args.validator:
        print("Started server as validator")
        PORT = random.randint(5001, 6000)
        pubsub = ValidatorPubSub(model_blockchain, train_pool, validation_pool)
        sync_model_blockchain(model_blockchain)
        sync_training_pool(train_pool)
        sync_validation_pool(validation_pool)

    elif args.miner:
        print("Started server as miner")
        PORT = random.randint(5001, 6000)
        pubsub = MinerPubSub(model_blockchain, train_pool, validation_pool)
        sync_model_blockchain(model_blockchain)
        sync_training_pool(train_pool)
        sync_validation_pool(validation_pool)
    else:
        print("Started server as root")
        pubsub = RootPubSub(blockchain=model_blockchain, 
        task_pool=task_pool, 
        train_pool=train_pool, 
        validation_pool=validation_pool,
        )

    set_pubsub(pubsub)
    print(PORT)
    app.run(host="0.0.0.0", port=PORT)


