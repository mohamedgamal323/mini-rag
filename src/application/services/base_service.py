import random
import string
import re

class BaseService:
    def generate_random_string(self, length: int = 12) -> str:        

        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name