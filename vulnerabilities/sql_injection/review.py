def flawed(table: dict = dict()) -> dict[tuple[str]]:
    table["PYTHON"] = (
        '''cursor.execute(f"INSERT INTO users (name, age) VALUES ('{name}','{age}')")''',
        '''query = f"SELECT * FROM users WHERE id = '{user_id}'"''',
        '''cursor.execute(f"INSERT INTO users (name, age) VALUES ("+name+","+age+")''',
        ''' query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)
cursor.execute(query)'''
    )
    return table

def fixed(table: dict = dict()) -> dict[tuple[str]]:
    table["PYTHON"] = (
        '''cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))''',
        '''query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))''',
        '''cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))''',
        '''query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))'''
    )
    return table
