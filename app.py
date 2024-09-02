from flask import Flask, jsonify, request
from flask_cors import CORS
import db_utils
import json
import config

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def get_shape_data():
    # shape = 'W12X53'
    input_str = request.json['text']
    shape = input_str

    with open('data/return_props.json', 'r') as file:
        return_props = json.load(file)
    with open('data/shape_table_labels.json', 'r') as file:
        prop_dict = json.load(file)
    search_column = return_props[0]
    shape_type = db_utils.return_shape_data(config.DATABASE_URL, config.TABLE_NAME, search_column, ['Type'], shape)[0]
    shape_props = db_utils.return_shape_data(config.DATABASE_URL, config.TABLE_NAME, search_column, return_props, shape)
    prop_labels = [prop_dict[prop]['label'] for prop in return_props]
    units = [prop_dict[prop]['units'] for prop in return_props]
    indices = [index for index, value in enumerate(shape_props) if value != "–"]
    filt_shape_props = [prop for index, prop in enumerate(shape_props) if index in indices]
    filt_prop_labels = [label for index, label in enumerate(prop_labels) if index in indices]
    filt_units = [unit for index, unit in enumerate(units) if index in indices]
    return jsonify({'prop_labels': filt_prop_labels, 'shape_props': filt_shape_props, 'units': filt_units, 'shape_type': shape_type})

@app.route('/shape-labels', methods=['GET'])
def get_labels():
    shape_header = 'EDI_Std_Nomenclature'
    shape_labels = db_utils.get_column_values(config.DATABASE_URL, config.TABLE_NAME, shape_header)
    return jsonify(shape_labels)

@app.route('/shape-table-labels', methods=['GET'])
def get_table_labels():
    with open('data/shape_table_labels.json', 'r') as file:
        shape_table_labels = json.load(file)
    return jsonify(shape_table_labels)

if __name__ == '__main__':
    app.run(debug=config.DEBUG)
