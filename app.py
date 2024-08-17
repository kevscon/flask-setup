from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

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

    db_name = 'data/shapes_database.db'
    table_name = 'shapes_database'
    search_column = 'EDI_Std_Nomenclature'
    return_columns = ['EDI_Std_Nomenclature', 'W', 'A', 'h', 'd', 'b', 'bf', 't', 'tdes', 'OD', 'ID', 'tw', 'tf', 'kdes', 'k1', 'T_toes', 'PB', 'x', 'y', 'Ix', 'Zx', 'Sx', 'rx', 'Iy', 'Zy', 'Sy', 'ry']
    # shape_type = return_shape_data(db_name, table_name, ['Type'], shape)[0]
    shape_list = return_shape_data(db_name, table_name, search_column, return_columns, shape)
    shape_dict = dict(zip(return_columns, shape_list))
    return jsonify(shape_dict)

@app.route('/shape-labels', methods=['GET'])
def shape_labels():
    db_name = 'data/shapes_database.db'
    table_name = 'shapes_database'
    shape_header = 'EDI_Std_Nomenclature'
    shape_labels = get_column_values(db_name, table_name, shape_header)
    return jsonify(shape_labels)

if __name__ == '__main__':
    app.run(debug=True)
