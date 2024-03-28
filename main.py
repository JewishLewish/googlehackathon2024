import google.generativeai as genai

class Const():
    generation_config = {"temperature":0.9, "top_p":1, "top_k":1}
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
    genai.configure(api_key="KEY")
    model = genai.GenerativeModel("gemini-pro", generation_config=generation_config, safety_settings=safety_settings)

class GenAI(Const):
    def gen(self, content) -> str:
        prompt_parts = [
            "flawedCode #example of sql injection\ncursor.execute(f\"INSERT INTO users (name, age) VALUES ('{name}','{age}')\")",
            "betterCode cursor.execute(\"INSERT INTO users (name, age) VALUES (?, ?)\", (name, age))",
            "flawedCode #example of sql injection\nquery = f\"SELECT * FROM users WHERE id = '{user_id}'\"",
            "betterCode query = \"SELECT * FROM users WHERE id = %s\"\ncursor.execute(query, (user_id,))",
            "flawedCode #example of insecure input handling\n@app.route(\"/search/",
            "betterCode from markupsafe import escape  # For escaping output; needed\n\n@app.route(\"/search/",
            "flawedCode #example of traversal path attack\nfrom flask import abort, Flask, request, send_file\nimport os\n\napp = Flask(__name__)\n\n@app.route('/download')\ndef download():\n  file = request.args.get('file', 'default.png')\n\n  if '..' in file:  # Basic path traversal check\n    abort(400, 'Directory Traversal Detected')\n\n  absolute_path = os.path.join(app.root_path, 'downloads', file)\n\n  if os.path.isfile(absolute_path):\n    return send_file(absolute_path)\n  else:\n    abort(404, 'Requested File Not Found')\n\napp.run()",
            "betterCode import os\nfrom flask import Flask, abort, request, send_file\nfrom werkzeug.utils import secure_filename\n\napp = Flask(__name__)\n\nDOWNLOADS_FOLDER = os.path.join(app.root_path, \"downloads\")  # Define download directory\n\n@app.route('/download')\ndef download():\n  # Get filename from query string\n  filename = request.args.get('file')\n\n  # Validate filename using secure_filename\n  if not filename or not secure_filename(filename):\n    return abort(400, \"Invalid filename\")\n\n  # Construct secure path within DOWNLOADS_FOLDER\n  filepath = os.path.join(DOWNLOADS_FOLDER, secure_filename(filename))\n\n  # Check if file exists within DOWNLOADS_FOLDER\n  if not os.path.exists(filepath):\n    return abort(404, \"Requested File Not Found\")\n\n  # Use send_file with the secure path\n  return send_file(filepath)\n\napp.run()",
            "flawedCode print(\"Hello world\")",
            "betterCode Nothing wrong.",
            "flawedCode #example of public confidential data\nusername = input(\"Enter username: \")\npassword = input(\"Enter password: \")\n\nif username == \"admin\" and password == \"secret\":\n  print(\"Login successful!\")\n  # Grant access to sensitive data or functionalities here\nelse:\n  print(\"Login failed.\")",
            "betterCode import os\n\nusername = input(\"Enter username: \")\npassword = input(\"Enter password: \")\n\nif username == \"admin\" and password == os.getenv(\"password\") :\n  print(\"Login successful!\")\n  # Grant access to sensitive data or functionalities here\nelse:\n  print(\"Login failed.\")",
            "flawedCode #example of public confidential data\nsecret = getUserInput()\n\nif secret == os.getenv(\"TEST_SECRET\"):\n    authenticateUser()",
            "betterCode secret = getUserInput()\n\nif secret == os.getenv(\"SECRET_PASSWORD\"):\n    authenticateUser()",
            "flawedCode #example of public confidential data - we want important data hidden\nauthKey = input(\"What is your key?\")\n\nif authKey == \"289023890328502395890\":\n    print(\"Door is opening...\")",
            "betterCode authKey = input(\"What is your key?\")\n\nif authKey == os.getenv(\"AUTH_KEY\"):\n    print(\"Door is opening...\")",
            f"flawedCode {content}",
            "betterCode ",
        ]


        return self.model.generate_content(prompt_parts).text


print(GenAI().gen("""print("hello world")

def helloUser(person):
    print("Hello "+person)           

secret = getUserInput()
    
if secret == "test":
    authenticateUser()
"""))