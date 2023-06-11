import random

def generate_guest_identifier():
    random_int = random.randint(10000, 99999)
    return f"Guest-{random_int}"


