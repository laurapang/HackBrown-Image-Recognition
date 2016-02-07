from flask import Flask
import sample

app = Flask(__name__)

@app.route('/')
def hello_world():
    return sample.match()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
