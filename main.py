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
    def gen(self, content) -> str:
        self.prompt_parts.append(f"PROBLEM {content}")
        self.prompt_parts.append("SOLUTION ")
        return self.model.generate_content(self.prompt_parts).text


gemini = GenAI()
output = gemini.gen("""
def get_user_by_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user
""")
