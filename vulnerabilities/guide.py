import importlib.util
import os
import numpy as np

class codeBlock():
    def __init__(self, code, type) -> None:
        self.code: str = code
        self.type: str = type
    
class Navigation():
    directories = ("sql_injection",)

    def go_through_directory(self):
        yield from (os.path.abspath(dir_name) for dir_name in self.directories)
    
    def numDir(self):
       return len(self.directories)

class TheBookofFlawed(Navigation):
    flawed: np.ndarray[codeBlock] = np.empty(len(Navigation.directories), dtype=codeBlock)
    fixed: np.ndarray[codeBlock] = np.empty(len(Navigation.directories), dtype=codeBlock)

    def __init__(self):
        for i, dir_path in enumerate(self.go_through_directory()):
            spec = importlib.util.spec_from_file_location("review", os.path.join(dir_path, "review.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Directly assign to the pre-allocated arrays
            self.flawed[i] = codeBlock(code=getattr(module, "flawed", None)(), type=dir_path)
            self.fixed[i] = codeBlock(code=getattr(module, "fixed", None)(), type=dir_path)


    def genPrompt(self):
        return {}

# Example usage
book = TheBookofFlawed()
print(book.flawed[0].code)