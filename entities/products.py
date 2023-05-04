from lib.filehandler import JSON, BIN
from utils.constants import OPTIONS_TODO

class Products:

    @staticmethod
    def buy_json(user):
        users = JSON.load_from_json()

        user.coins = users[user.name]['coins']

        print(user.coins)

        while True:
            print('1. Рыбка - 15 монет'
                  '\n2. Косточка - 15 монеток'
                  '\n3. Выход')

            choice = input('Номер выбора: ')
            if choice == '1':
                if user.coins < 15:
                    print('У Вас недостаточно монеток!')

                else:
                    user.items['FISH'] += 1
                    user.coins -= 15

                    users = JSON.load_from_json()

                    users[user.name]['items'] = user.items
                    users[user.name]['coins'] -= 15

                    JSON.dump_to_json(users)

            elif choice == '2':
                if user.coins < 15:
                    print('У Вас недостаточно монеток!')

                else:
                    user.items['BONE'] += 1
                    user.coins -= 15

                    users = JSON.load_from_json()

                    users[user.name]['items'] = user.items
                    users[user.name]['coins'] -= 15

                    JSON.dump_to_json(users)

            elif choice == '3':
                print(OPTIONS_TODO)
                break
            else:
                print('Неправильный выбор, попробуйте еще раз!')

    @staticmethod
    def buy_bin(user):
        users = BIN.load_from_bin()

        user.coins = users[user.name]['coins']

        print(user.coins)

        while True:
            print('1. Рыбка - 15 монет'
                  '\n2. Косточка - 15 монеток'
                  '\n3. Выход')

            choice = input('Номер выбора: ')
            if choice == '1':
                if user.coins < 15:
                    print('У Вас недостаточно монеток!')

                else:
                    user.items['FISH'] += 1
                    user.coins -= 15

                    users = BIN.load_from_bin()

                    users[user.name]['items'] = user.items
                    users[user.name]['coins'] -= 15

                    BIN.dump_to_bin(users)

            elif choice == '2':
                if user.coins < 15:
                    print('У Вас недостаточно монеток!')

                else:
                    user.items['BONE'] += 1
                    user.coins -= 15

                    users = BIN.load_from_bin()

                    users[user.name]['items'] = user.items
                    users[user.name]['coins'] -= 15

                    BIN.dump_to_bin(users)

            elif choice == '3':
                break
            else:
                print('Неправильный выбор, попробуйте еще раз!')

