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
        return self.model.generate_content(genPrompt).text
    
    def guessLang(self, code:str) -> str:
        prompt = f"""Look at the following code: \n{code}\nWhat programming language is this? Output answer in all caps."""
        return self.model.generate_content(prompt).text


gemini = GenAI()
output = gemini.gen("""
Role: You are a security analysis, focused on software, tasked to look at code and improve the security of it.

Input:

You will be presented a block of code.

Constraints:

You cannot access any external information or knowledge base.
Your solutions must be based solely on the information provided in the PROBLEM statements and the previous SOLUTION(S).

Output:      
Output must be in valid JSON format.
{
    "PROBLEM_TYPE":"{type of problem; if no problem then N\A}",
    "SOLUTION":"{updated code with problem fixed; if no problem then N\A}"
}
             
The Code:           

```
print("Hello world")
```

""")
print(output)

