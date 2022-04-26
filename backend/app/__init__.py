from flask import Flask

from backend.blockchain.blockchain import Blockchain
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return 'The beginning of everything'

@app.route('/test')
def test():
    return 'Ilker Baba'

@app.route('/blockchain')
def route_blockchain():
    df = blockchain.chain_df()
    return df.to_html()


app.run(port=3001)
