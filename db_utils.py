import sqlite3

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