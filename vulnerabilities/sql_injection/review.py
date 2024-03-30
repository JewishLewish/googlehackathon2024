

def flawed() -> dict[tuple[str]]:
    table:dict = dict()
    table["PYTHON"] = (
        '''cursor.execute(f"INSERT INTO users (name, age) VALUES ('{name}','{age}')")''', 
        '''query = f"SELECT * FROM users WHERE id = '{user_id}'"''',
        '''cursor.execute(f"INSERT INTO users (name, age) VALUES ("+name+","+age+")'''
    )
    return table

def fixed() -> dict[tuple[str]]:
    table = dict()
    table["PYTHON"] = (
        '''cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))''',
        '''query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))''',
        '''cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))'''
    )
    return table