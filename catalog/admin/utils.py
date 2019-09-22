import csv
import random
import string


def random_password_generator(password_length=8):
    letters = string.ascii_letters + ''.join([str(idx) for idx in range(10)])
    password = []
    for _ in range(password_length):
        password.append(random.choice(letters))
    return ''.join(password)


def process_file(file):
    with open(file, 'r') as file:
        csv_reader = csv.DictReader(file)
