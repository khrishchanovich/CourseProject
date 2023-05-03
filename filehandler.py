import datetime

import todolist
import os
from user import User
from pet import Pet
from task import Task, Status, Category
import json



class JSON:
    @staticmethod
    def load_from_json():
        with open('users.json', 'r') as f:
            users = json.load(f)

        return users

    @staticmethod
    def dump_to_json(users):
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)

    def run(self):
        users = JSON.load_from_json()

        for name in users:
            print(f'User: {name}')



class BIN:
    @staticmethod
    def load_from_bin():
        pass

    @staticmethod
    def dump_to_bin(users):
        pass


class FileHandler:
    pass
