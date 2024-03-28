import importlib.util
import os

class codeBlock():
    def __init__(self, code, type) -> None:
        self.code: str = code
        self.type: str = type
    
class Navigation():
    directories = ("sql_injection",)

    def go_through_directory(self):
        for dir_name in self.directories:
            dir_path = os.path.abspath(dir_name)
            yield dir_path

class TheBookofFlawed(Navigation):
    flawed:list[codeBlock] = []
    fixed:list[codeBlock] = []

    def __init__(self):
        for dir_path in self.go_through_directory():
            spec = importlib.util.spec_from_file_location("review", os.path.join(dir_path, "review.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.flawed.append(codeBlock(code=getattr(module, "flawed", None)(),type=dir_path))
            self.fixed.append(codeBlock(code=getattr(module, "fixed", None)(),type=dir_path))

    def genPrompt(self):
        return {}

# Example usage
book = TheBookofFlawed()
print(book.flawed[0].code)
print(book.fixed)