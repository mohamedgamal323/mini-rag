import random
import string
import re

class BaseService:
    def generate_random_string(self, length: int = 12) -> str:        

        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    