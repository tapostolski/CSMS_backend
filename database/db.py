import sqlite3

class BaseDbConnection:
    def __init__(self):
        """initialize mysql db and/or connection"""
        self.conn = sqlite3.connect('SMM_System.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    
#duh
def generate_update_query_string_from_data(input_data: dict):
    """generates strings for UPDATE query from input data"""
    keys = input_data.keys()
    values = input_data.values()
    kvp = zip(keys, values)
    
    input_to_query = []
    for pair in kvp:
        input_to_query.append(f'{pair[0]} = "{pair[1]}"')
    query_input_string = ', '.join(input_to_query)

    return query_input_string