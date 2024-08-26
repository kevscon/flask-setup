from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import config

app = Flask(__name__)
CORS(app)

def return_shape_data(db_name, table_name, search_column, return_columns, value):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    columns_str = ", ".join(return_columns)
    query = f"SELECT {columns_str} FROM {table_name} WHERE {search_column} = ?"
    cursor.execute(query, (value,))
    filtered_rows = list(cursor.fetchall()[0])
    conn.close()
    return filtered_rows

def get_column_values(db_name, table_name, column_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)
    values = [row[0] for row in cursor.fetchall()]
    conn.close()
    return values

@app.route('/', methods=['POST'])
def get_shape_data():
    # shape = 'W12X53'
    input_str = request.json['text']
    shape = input_str

    with open('data/return_props.json', 'r') as file:
        return_props = json.load(file)
    search_column = return_props[0]
    # shape_type = return_shape_data(config.DATABASE_URL, config.TABLE_NAME, ['Type'], shape)[0]
    shape_list = return_shape_data(config.DATABASE_URL, config.TABLE_NAME, search_column, return_props, shape)
    shape_dict = dict(zip(return_props, shape_list))
    return jsonify(shape_dict)

@app.route('/shape-labels', methods=['GET'])
def get_labels():
    shape_header = 'EDI_Std_Nomenclature'
    shape_labels = get_column_values(config.DATABASE_URL, config.TABLE_NAME, shape_header)
    return jsonify(shape_labels)

@app.route('/shape-table-labels', methods=['GET'])
def get_table_labels():
    with open('data/shape_table_labels.json', 'r') as file:
        shape_table_labels = json.load(file)
    return jsonify(shape_table_labels)

if __name__ == '__main__':
    app.run(debug=config.DEBUG)
