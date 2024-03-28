import importlib.util
import os
import numpy as np

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
        yield from (os.path.abspath(dir_name) for dir_name in self.directories)
    
    def numDir(self):
       return len(self.directories)

class TheBookofFlawed(Navigation):
    solutions: np.ndarray[codeBlock] = np.empty(1, dtype=codeBlock)

    def __init__(self):
        solutions:list[codeBlock] = []
        for dir_path in self.go_through_directory():
            spec = importlib.util.spec_from_file_location("review", os.path.join(dir_path, "review.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for x, y in getattr(module, "flawed", None)(), getattr(module, "fixed", None)():
                solutions.append(codeBlock(flawed=x, fixed=y, type=dir_path.split("""\\""")[-1]   ))

        self.solutions = np.array(solutions)

    def genPrompt(self):
        return {}

# Example usage
book = TheBookofFlawed()
print(book.solutions[0])