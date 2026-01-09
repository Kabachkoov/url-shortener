import hashlib
import string
import random


def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_short_code_from_url(url: str, length: int = 6):
    hash_object = hashlib.md5(url.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:length]
