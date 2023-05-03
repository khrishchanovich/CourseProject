import pickle

from user import User
import os
import json
import xml.etree.ElementTree as ET

"""Class RegistrationPolicy"""


class RegistrationPolicy:

    @staticmethod
    def register_json(name, password, pet, coins):
        with open('users.json', 'r') as file:
            users = json.load(file)
            users[name] = {'password': password, 'pet': pet, 'coins': coins, 'items': {'FISH': 0, 'BONE': 0},
                           'todo_task': []}
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def register_bin(name, password, pet, coins):
        with open('users.bin', 'rb') as file:
            if os.path.getsize('users.bin') != 0:
                users = pickle.load(file)
            else:
                users = {}
            users[name] = {'password': password, 'pet': pet, 'coins': coins, 'items': {}, 'todo_task': []}
            with open('users.bin', 'wb') as file:
                pickle.dump(users, file, protocol=3)



