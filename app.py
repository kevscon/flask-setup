from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def submit_text():
    input_data = request.json
    text_input = input_data.get('text', '')
    return jsonify({'message': text_input + '!'})

if __name__ == '__main__':
    app.run(debug=True)
