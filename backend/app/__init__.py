from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'The beginning of everything'
@app.route('/test')
def test():
    return 'Ilker Baba'


app.run(port=3001)
