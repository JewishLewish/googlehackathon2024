def flawed() -> str:
    return ('''cursor.execute(f"INSERT INTO users (name, age) VALUES ('{name}','{age}')")''')

def fixed() -> str:
    return ('''cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))''')