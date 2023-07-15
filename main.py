import random
import string
from art import *
from threading import Thread, Lock
from termcolor import colored
import requests
from colorama import init
init()

NUM_KEYS_PER_SECOND = 100

def generate_random_code():
    characters = string.ascii_uppercase + string.digits
    code = '-'.join(''.join(random.choice(characters) for _ in range(5)) for _ in range(5))
    return code

def generate_key(key, lock):
    response = requests.get(f'https://partner.steam-api.com/ISteamCDKey/Check?format=json&key={API_KEY}&cdkey={key}')
    if response.status_code == 200:
        data = response.json()
        if 'error' not in data:
            valid_key = key
            color = random.choice(['red', 'yellow', 'green', 'blue', 'magenta'])
            with lock:
                print(colored(valid_key, color) + ": Valid")
                save_valid_key(valid_key)
        else:
            invalid_key = key
            color = random.choice(['red', 'yellow', 'green', 'blue', 'magenta'])
            with lock:
                print(colored(invalid_key, color) + ": Invalid")
    else:
        error_key = key
        color = random.choice(['red', 'yellow', 'green', 'blue', 'magenta'])
        with lock:
            print(colored(error_key, color) + ": Error - Invalid Response")

def generate_keys_continuous():
    welcome_banner = text2art("Welcome to STEAMKG", font="small")
    print(welcome_banner)

    lock = Lock()

    while True:
        threads = []
        for _ in range(NUM_KEYS_PER_SECOND):
            key = generate_random_code()
            thread = Thread(target=generate_key, args=(key, lock))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

def save_valid_key(key):
    with open("output.txt", "a") as file:
        file.write(key + "\n")

def save_api_key(api_key):
    with open("steamapikey.txt", "w") as file:
        file.write(api_key)

try:
    with open("steamapikey.txt", "r") as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    API_KEY = input("Enter your Steam API key: ")
    save_api_key(API_KEY)

print("Press Enter to start key generation...")
input()

generate_keys_continuous()
