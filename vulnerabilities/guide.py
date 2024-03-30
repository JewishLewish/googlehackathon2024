#from utilities.id import identifiers
import importlib.util
import os
import numpy as np

class identifiers():
    PYTHON = "PYTHON"

    def all(self) -> list:
        return ["PYTHON"]


class codeBlock():
    def __init__(self, flawed, fixed, type) -> None:
        self.problem: str = flawed
        self.solution: str = fixed
        self.type: str = type
    
    def __str__(self) -> str:
        return f'''Problem:\t{self.problem}\nSolution:\t{self.solution}\nType:\t\t{self.type}'''
    
class Navigation():
    directories = ("sql_injection",)

    def go_through_directory(self):
        yield from (os.path.abspath("vulnerabilities\\" + dir_name) for dir_name in self.directories)

    
    def numDir(self):
       return len(self.directories)

class TheBookofFlawed(Navigation):
    solutionsAll = {lang: [] for lang in identifiers().all()}


    def __init__(self):
        for dir_path in self.go_through_directory():
            spec = importlib.util.spec_from_file_location("review", os.path.join(dir_path, "review.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            flawed: dict = getattr(module, "flawed", None)()
            fixed: dict = getattr(module, "fixed", None)()
            for lang in identifiers().all():
                self.solutionsAll[lang].append(codeBlock(flawed=flawed[lang], fixed=fixed[lang], type=dir_path.split("""\\""")[-1]))
            #for x, y in zip(flawed, fixed):
            #    solutions.append(codeBlock(flawed=x, fixed=y, type=dir_path.split("""\\""")[-1]   ))


    def genPrompt(self):
        prompt_part = {lang: [] for lang in identifiers().all()}
        
        for lang in identifiers().all():
            for code in self.solutionsAll[lang]:
                prompt_part[lang].append(f"PROBLEM #Problem:{code.type}\n {code.problem}")
                prompt_part[lang].append(f"SOLUTION {code.solution}")

        #prompt_part: list[str] = []
        #for code in self.solutionsAll[lang]:
        #    prompt_part.append(f"PROBLEM #Problem:{code.type}\n {code.problem}")
        #    prompt_part.append(f"SOLUTION {code.solution}")
        
        return prompt_part