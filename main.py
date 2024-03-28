import google.generativeai as genai
import vulnerabilities.guide

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
    genai.configure(api_key=None)
    model = genai.GenerativeModel("gemini-pro", generation_config=generation_config, safety_settings=safety_settings)

class GenAI(Const):
    prompt_parts = vulnerabilities.guide.TheBookofFlawed().genPrompt()
    def gen(self, content) -> str:
        self.prompt_parts.append(f"flawedCode {content}")
        self.prompt_parts.append("betterCode ")
        return self.model.generate_content(self.prompt_parts).text


print(GenAI().gen(""" cursor.execute(f"INSERT INTO users (name, age) VALUES ("+name+","+age+")")
                  Two word. What is wrong with code?
"""))