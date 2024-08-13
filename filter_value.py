import sqlite3

def filter_table_by_column_value(db_name, table_name, column_name, value):
    """
    Filter data from an SQLite table based on a matching value in a specific column.

    :param db_name: The name of the SQLite database file.
    :param table_name: The name of the table to filter.
    :param column_name: The name of the column to filter by.
    :param value: The value to match in the specified column.
    :return: A list of tuples containing the filtered rows.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the SELECT statement with filtering based on the column value
    query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"

    # Execute the query with the provided value
    cursor.execute(query, (value,))

    # Fetch all the filtered rows
    filtered_rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return filtered_rows

# Example usage
db_name = 'example.db'
table_name = 'my_table'
column_name = 'name'
value = 'Jane Doe'

filtered_data = filter_table_by_column_value(db_name, table_name, column_name, value)
for row in filtered_data:
    print(row)
