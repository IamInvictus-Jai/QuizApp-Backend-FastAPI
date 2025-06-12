from os import path
from json import loads

class LoadInstructions:
    def __init__(self, base_filename:str = 'app/system_instructs'):
        self.base_path = base_filename
        self.cache = {} # Store the loaded instructions to avoid loading them multiple times
    
    def load(self, file_name:str):

        if not path.exists(f"{self.base_path}/{file_name}"): raise FileNotFoundError
        if file_name in self.cache: return self.cache[file_name]

        if file_name.endswith('.json'):
            self.cache[file_name] = self.load_json(file_name)
            return self.cache[file_name]         
        elif file_name.endswith('.txt'):
            self.cache[file_name] = self.load_text(file_name)
            return self.cache[file_name]
            
        raise NotImplementedError
    
    def load_json(self, file_name:str):
        try:
            with open(f"{self.base_path}/{file_name}", 'r', encoding='utf-8') as f:
                return loads(f.read())
        except UnicodeDecodeError:
            # Fallback to read with a different encoding if UTF-8 fails
            with open(f"{self.base_path}/{file_name}", 'r', encoding='latin-1') as f:
                return loads(f.read())
    
    def load_text(self, file_name:str):
        """
        Reads a text file and returns its content as a string.

        :param file_name: The name of the text file to read
        :return: The content of the file
        """
        try:
            with open(f"{self.base_path}/{file_name}", 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback to read with a different encoding if UTF-8 fails
            with open(f"{self.base_path}/{file_name}", 'r', encoding='latin-1') as f:
                return f.read()