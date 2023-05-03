import os.path

from storage import Storage, EItem
import json
import pickle
from filehandler import JSON


class Products:

    @staticmethod
    def buy_json(user):
        with open('users.json', 'r') as file:
            users = json.load(file)

        user.coins = users[user.name]['coins']

        print(user.coins)

        while True:
            print('1. Buy fish'
                  '\n2. Buy bone'
                  '\n3. Exit')

            choice = input('Enter choice: ')
            if choice == '1':
                if user.coins < 15:
                    print('You have no enough coins!')

                else:
                    user.items['FISH'] += 1
                    user.coins -= 15

                    with open('users.json', 'r') as file:
                        users = json.load(file)
                    # users = JSON.load_from_json()

                    users[user.name]['items'] = user.items
                    users[user.name]['coins'] -= 15

                    with open('users.json', 'w') as file:
                        json.dump(users, file, indent=4)
                    # JSON.dump_to_json(users)

            elif choice == '2':
                if user.coins < 15:
                    print('You have no enough coins!')

                else:
                    user.items['BONE'] += 1
                    user.coins -= 15

                    users = JSON.load_from_json()

                    users[user.name]['items'] = user.items
                    users[user.name]['coins'] -= 15

                    JSON.dump_to_json(users)

            elif choice == '3':
                break
            else:
                print('Invalid choice, try again!')

    @staticmethod
    def buy_bin(user):
        with open('users.bin', 'rb') as file:
            if os.path.getsize('users.bin') != 0:
                users = pickle.load(file)
            else:
                users = {}

        user.coins = users[user.name]['coins']

        print(user.coins)

        while True:
            print('1. Buy fish'
                  '\n2. Buy bone'
                  '\n3. Exit')

            choice = input('Enter choice: ')
            if choice == '1':
                if user.coins < 15:
                    print('You have no enough coins!')

                else:
                    user.items['FISH'] += 1
                    user.coins -= 15

                    with open('users.bin', 'rb') as file:
                        if os.path.getsize('users.bin') != 0:
                            users = pickle.load(file)
                        else:
                            users = {}

                    users[user.name]['items'] = user.items
                    users[user.name]['coins'] -= 15

                    with open('users.bin', 'wb') as f:
                        pickle.dump(users, f, protocol=3)

            elif choice == '2':
                if user.coins < 15:
                    print('You have no enough coins!')

                else:
                    user.items['BONE'] += 1
                    user.coins -= 15

                    with open('users.bin', 'rb') as file:
                        if os.path.getsize('users.bin') != 0:
                            users = pickle.load(file)
                        else:
                            users = {}

                    users[user.name]['items'] = user.items
                    users[user.name]['coins'] -= 15

                    with open('users.bin', 'wb') as f:
                        pickle.dump(users, f, protocol=3)

            elif choice == '3':
                break
            else:
                print('Invalid choice, try again!')

