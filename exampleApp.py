from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/elmo/')
def elmo_meeting():
    return 'ELMO MEETING! ELMO MEETING! THIS CODE IS VERY RELEVANT!'
