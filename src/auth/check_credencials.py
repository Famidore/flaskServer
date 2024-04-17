import re


def validate_email(input: str):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    return bool(re.fullmatch(regex, input))


def validate_password(input: str):
    """
    8 char long
    1 uppercase
    1 lowercase
    1 digit
    """
    regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    return bool(re.match(regex, input))
