def flawed() -> str:
    return ('''cursor.execute(f"INSERT INTO users (name, age) VALUES ('{name}','{age}')") | query = f"SELECT * FROM users WHERE id = '{user_id}'"''')

def fixed() -> str:
    return ('''cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age)) | query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))''')