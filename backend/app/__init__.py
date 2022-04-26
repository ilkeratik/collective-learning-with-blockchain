import os, random
from flask import Flask, jsonify, request

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
    return 'Ilker Baba'

@app.route('/blockchain')
def route_view_blockchain():
    df = blockchain.chain_df()
    return df.to_html()

@app.route('/api/blockchain')
def route_json_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/api/blockchain/mine/<data>', methods=['POST', 'GET' ])
def route_mine_block(data):
    try:
        if request.method == 'GET':
            blockchain.add_block(data)
        if request.method == 'POST':
            post_body = request.form
            print(post_body)
            blockchain.add_block(post_body.data)

        block = blockchain.chain[-1]
        pubsub.broadcast_block(block)
        return f'Successfully added block to blockchain, data={data}'
    except Exception as e:
        return e, 500


PORT = 5000
print(os.environ.get('PEER') )
if os.environ.get('PEER') == 'True':
    
    PORT = random.randint(5001, 6000)
app.run(port=PORT)
