import json
import secret
import google.generativeai as genai
import vulnerabilities.guide

class Const():
    generation_config = {"temperature":.95, "top_p":1, "top_k":1}
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
    genai.configure(api_key=secret.key)
    model = genai.GenerativeModel("gemini-pro", generation_config=generation_config, safety_settings=safety_settings)

class GenAI(Const):
    prompt_parts = vulnerabilities.guide.TheBookofFlawed().genPrompt()

    def gen(self, content, lang: str = vulnerabilities.guide.identifiers().PYTHON) -> str:
        genPrompt = self.prompt_parts[lang]
        genPrompt.append(f"PROBLEM {content}")
        genPrompt.append("SOLUTION ")
        print(genPrompt)
        return self.model.generate_content(genPrompt).text
    
    def guessLang(self, code:str) -> str:
        prompt = f"""Look at the following code: \n{code}\nWhat programming language is this? Output answer in all caps."""
        return self.model.generate_content(prompt).text


gemini = GenAI()
output = gemini.gen("""
Task:  Solve a series of problems using the knowledge gained from previous solutions.

Role: You are a security analysis, focused on software, tasked to look at code and improve the security of it.

Input:

You will be presented a block of code.

Constraints:

You cannot access any external information or knowledge base.
Your solutions must be based solely on the information provided in the PROBLEM statements and the previous SOLUTION(S).
You must output the entire code block with the modified solution. If everything is secure then write "DO NOTHING!"

The Code:           
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Vulnerable endpoint rendering HTML template with unsanitized input
@app.route('/')
def index():
    return "Hello world"

if __name__ == '__main__':
    app.run(debug=True)

""")
print(output)


['PROBLEM #Problem:sql_injection\n (\'cursor.execute(f"INSERT INTO users (name, age) VALUES (\\\'{name}\\\',\\\'{age}\\\')")\', \'query = f"SELECT * FROM users WHERE id = \\\'{user_id}\\\'"\', \'cursor.execute(f"INSERT INTO users (name, age) VALUES ("+name+","+age+")\', \' query = "SELECT * FROM users WHERE username = \\\'{}\\\' AND password = \\\'{}\\\'".format(username, password)\\ncursor.execute(query)\')', 'SOLUTION (\'cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))\', \'query = "SELECT * FROM users WHERE id = %s"\\ncursor.execute(query, (user_id,))\', \'cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))\', \'query = "SELECT * FROM users WHERE username = ? AND password = ?"\\ncursor.execute(query, (username, password))\')', "PROBLEM #Problem:web_development\n #doesn't exist; flask", "SOLUTION @app.after_request\ndef add_header(response):\n    response.headers['X-Content-Type-Options'] = 'nosniff'\n    return response", 'PROBLEM Using previous PROBLEM and SOLUTION as your guide. If nothing can be done, write "DO NOTHING!"\n                    \nfrom flask import Flask, render_template_string, request\n\napp = Flask(__name__)\n\n# Vulnerable endpoint rendering HTML template with unsanitized input\n@app.route(\'/\')\ndef index():\n    name = request.args.get(\'name\')\n    return render_template_string(\'{{ name }}\', name=name)\n\nif __name__ == \'__main__\':\n    app.run(debug=True)\n', 'SOLUTION ']