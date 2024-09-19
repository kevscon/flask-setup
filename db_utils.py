import sqlite3

def get_unique_column_values(db_name, table_name, column_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = f"SELECT DISTINCT {column_name} FROM {table_name}"
    cursor.execute(query)
    unique_values = cursor.fetchall()
    conn.close()
    return [value[0] for value in unique_values]

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

def filter_shape_data(db_name, table_name, return_columns, **kwargs):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    columns_str = ", ".join(return_columns)
    conditions = []
    values = []
    
    for column, value in kwargs.items():
        if isinstance(value, list) and len(value) == 2:
            min_value, max_value = value
            
            # Allow all values if min_value or max_value is an empty string
            if min_value == "" and max_value == "":
                continue  # Exclude this condition
            elif min_value == "":
                conditions.append(f"CAST({column} AS FLOAT) <= ?")
                values.append(max_value)
            elif max_value == "":
                conditions.append(f"CAST({column} AS FLOAT) >= ?")
                values.append(min_value)
            else:
                conditions.append(f"CAST({column} AS FLOAT) BETWEEN ? AND ?")
                values.extend([min_value, max_value])
        elif isinstance(value, str):
            conditions.append(f"{column} = ?")
            values.append(value)
        else:
            raise ValueError(f"Unsupported value type for column '{column}': {type(value)}")
    
    # If there are no conditions, return all rows
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"SELECT {columns_str} FROM {table_name} WHERE {where_clause}"
    cursor.execute(query, tuple(values))
    filtered_rows = cursor.fetchall()
    conn.close()
    return filtered_rows