import os, random
from flask import Flask, jsonify, request
import requests
from backend.pubsub import PubSub
from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)

@app.route('/')
def index():
    return 'The beginning of everything'

@app.route('/test')
def test():
    return 'Ilker'

@app.route('/blockchain')
def route_view_blockchain():
    df = blockchain.chain_df()
    return df.to_html()

@app.route('/api/blockchain')
def route_json_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/api/blockchain/mine/<data>', methods=[ 'GET' ])
def route_mine_block_get(data):
    try:
        blockchain.add_block(data)

        block = blockchain.chain[-1]
        pubsub.broadcast_block(block)
        return f'Successfully added block to blockchain, data={data}'
    except Exception as e:
        return e, 500

@app.route('/api/blockchain/mine', methods=[ 'POST' ])
def route_mine_block():
    try:
        post_body = request.form
        data = post_body['data']
        print(post_body)
        blockchain.add_block(data)

        block = blockchain.chain[-1]
        pubsub.broadcast_block(block)
        return f'Successfully added block to blockchain, data={data} ', 200
    except Exception as e:
        return e, 500


ROOT_PORT = 5000
PORT = 5001

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)
    res = requests.get(f'http://localhost:{ROOT_PORT}/api/blockchain') #sync latest blockchain
    print(f'result: {res.json()}')

    res_blockchain = Blockchain.from_json(res.json())
    try:
        blockchain.replace_chain(res_blockchain.chain)
        print('\n -- Successfully synchronized the local chain')
    except Exception as e:
        print(f'Error when syncing: {e}')
app.run(port=PORT)
