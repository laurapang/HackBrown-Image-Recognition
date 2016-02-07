from flask import Flask
from sample import match

app = Flask(__name__)

@app.route('/')
def hello_world():
    return match()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
