import json
import os
import pickle


class JSON:
    @staticmethod
    def load_from_json(username):
        with open(f'users/{username}.json', 'r') as fr:
            users = json.load(fr)

        return users

    @staticmethod
    def dump_to_json(users, username):
        with open(f'users/{username}.json', 'w') as fw:
            json.dump(users, fw, indent=4)

    @staticmethod
    def register_json(name, password, pet, coins):
        with open('D:/CourseProject/users/users.json', 'r') as file:
            users = json.load(file)
            users[name] = {'password': password, 'pet': pet, 'coins': coins, 'items': {'FISH': 0, 'BONE': 0},
                           'todo_task': []}
        with open('D:/CourseProject/users/users.json', 'w') as file:
            json.dump(users, file, indent=4)


class BIN:
    @staticmethod
    def load_from_bin():
        with open('D:/CourseProject/users/users.bin', 'rb') as file:
            if os.path.getsize('D:/CourseProject/users/users.bin') != 0:
                users = pickle.load(file)
            else:
                users = {}

        return users

    @staticmethod
    def dump_to_bin(users):
        with open('D:/CourseProject/users/users.bin', 'wb') as f:
            pickle.dump(users, f, protocol=3)

    @staticmethod
    def register_bin(name, password, pet, coins):
        with open('D:/CourseProject/users/users.bin', 'rb') as file:
            if os.path.getsize('D:/CourseProject/users/users.bin') != 0:
                users = pickle.load(file)
            else:
                users = {}
            users[name] = {'password': password, 'pet': pet, 'coins': coins, 'items': {'FISH': 0, 'BONE': 0},
                           'todo_task': []}
        with open('D:/CourseProject/users/users.bin', 'wb') as file:
            pickle.dump(users, file, protocol=3)


