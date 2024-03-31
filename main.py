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
        genPrompt[lang].append(f"PROBLEM {content}")
        genPrompt[lang].append("SOLUTION ")
        return self.model.generate_content(genPrompt).text
    
    def guessLang(self, code:str) -> str:
        prompt = f"""Look at the following code: \n{code}\nWhat programming language is this? Output answer in all caps."""
        return self.model.generate_content(prompt).text


gemini = GenAI()
output = gemini.guessLang("""
class GenAI(Const):
    prompt_parts = vulnerabilities.guide.TheBookofFlawed().genPrompt()
    def gen(self, content, lang: str = vulnerabilities.guide.identifiers().PYTHON) -> str:
        self.prompt_parts[lang].append(f"PROBLEM {content}")
        self.prompt_parts[lang].append("SOLUTION ")
        return self.model.generate_content(self.prompt_parts[lang]).text""")
print(output)