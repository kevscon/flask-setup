from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/reverse', methods=['POST'])
def reverse_text():
    data = request.json
    text = data.get('text', '')
    reversed_text = text[::-1]
    return jsonify({'reversed_text': reversed_text})

if __name__ == '__main__':
    app.run(debug=True)
