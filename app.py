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
    filtered_rows = cursor.fetchall()
    conn.close()
    return filtered_rows

@app.route('/', methods=['POST'])
def get_shape_data():
    # shape = 'W12X53'
    input_str = request.json['text']
    shape = input_str.upper()

    db_name = 'data/shapes_database.db'
    table_name = 'shapes_database'
    search_column = 'EDI_Std_Nomenclature'
    return_columns = ['EDI_Std_Nomenclature', 'W', 'A', 'h', 'd', 'b', 'bf', 't', 'tdes', 'OD', 'ID', 'tw', 'tf', 'kdes', 'k1', 'T_toes', 'PB', 'x', 'y', 'Ix', 'Zx', 'Sx', 'rx', 'Iy', 'Zy', 'Sy', 'ry']
    # display_labels = ['Shape', 'Weight', 'Area', 'h', 'd', 'b', 'b<sub>f</sub>', 't', 't_des', 'OD', 'ID', 't_w', 't_f', 'k_des', 'k_1', 'T', 'PB', 'x_bar', 'y_bar', 'Ix', 'Zx', 'Sx', 'rx', 'Iy', 'Zy', 'Sy', 'ry']
    shape_list = return_shape_data(db_name, table_name, search_column, return_columns, shape)
    shape_dict = dict(zip(return_columns, shape_list[0]))
    return jsonify(shape_dict)

if __name__ == '__main__':
    app.run(debug=True)
