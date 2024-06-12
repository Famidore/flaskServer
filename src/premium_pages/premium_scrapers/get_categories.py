import random
import string


def get_categories(quantity: int = 10):
    letters = string.ascii_lowercase
    # testing
    return [
        "".join(random.choice(letters) for i in range(5)) for word in range(quantity)
    ]


if __name__ == "__main__":
    print(get_categories(10))
