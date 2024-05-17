import random
import string

def generate_random_alphanumeric():
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    random_string = ''.join(random.choices(characters, k=9))
    return random_string

# Exemple d'utilisation
