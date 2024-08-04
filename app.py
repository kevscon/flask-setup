from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    input_message = 'Hello, World!'
    return jsonify({'message': input_message})

if __name__ == '__main__':
    app.run(debug=True)