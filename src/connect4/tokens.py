from random import choice
from string import ascii_lowercase, ascii_uppercase, digits

allowed_characters = ascii_lowercase + ascii_uppercase + digits


def generate_token(length: int) -> str:
    return "".join(choice(allowed_characters) for _ in range(length))
