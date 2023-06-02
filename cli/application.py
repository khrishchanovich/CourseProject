import sys

from utils.constants import RULES, \
    OPTIONS_TODO, OPTIONS_UPDATE, OPTIONS_EDIT_TASK,\
    QUESTION, QUESTION_FOOD, CONTINEU_QUESTION,\
    CATEGORY, TYPE_ITEM, PROBLEM, \
    Animal
from entities.task import Task, Status, Category
from entities.user import User
from entities.animal import Type
from entities.pet import Pet
from entities.storage import Storage
from entities.products import Products
from entities.registationpolicy import RegistrationPolicy

from lib.filehandler import JSON, BIN

import datetime


class ApplicationJSON:

    def run(self):
        users = JSON.load_from_json()

        for name in users:
            print(f'Пользователь: {name}')

        print(QUESTION)

        while True:
            choice = input()

            if choice == '1':
                self.login()
                break
            elif choice == '2':
                self.register()
                break
            else:
                print('Неправильный выбор, попробуйте еще раз!')

    def login(self):
        name = input('Введите имя: ')
        password = input('Введите пароль: ')

        users = JSON.load_from_json()

        if name not in users:
            print(PROBLEM)
            self.run()

        if name in users and users[name]['password'] == password:
            coins = users[name]['coins']
            items = users[name]['items']
            pet = users[name]['pet']

            self.user = User(name, password, pet, coins, items)
            list_ = users[name]['todo_task']

            print(coins)

            for i in list_:
                task = Task()
                task.set_title(i['name'])

                if i['status'] == Status.DONE.name:
                    task.set_status(Status.DONE)
                else:
                    task.set_status(Status.PENDING)
                if i['category'] == Category.NONE.name:
                    task.set_category(Category.NONE)
                elif i['category'] == Category.DAILY.name:
                    task.set_category(Category.DAILY)
                elif i['category'] == Category.WORKING.name:
                    task.set_category(Category.WORKING)
                elif i['category'] == Category.LEARNING.name:
                    task.set_category(Category.LEARNING)
                elif i['category'] == Category.TRAVELING.name:
                    task.set_category(Category.TRAVELING)
                else:
                    task.set_category(Category.PERSONAL)

                task.set_date_of_created(i['creation_time'])
                task.set_price(i['price'])

                self.user.todo.add_to_do(task)

        elif name in users and users[name]['password'] != password:
            print('Вы ввели неправильный пароль :(\nПопробуйте еще раз!')
            self.login()

        self.response()

    def register(self):
        name = input('Введите имя: ')

        # users = JSON.load_from_json()
        #
        # if name in users:
        #     print('Такое имя пользователя уже существует :(\n'
        #           'Попробуйте ввести другое имя для регистрации')
        #     self.register()

        password = input('Введите пароль: ')
        pet_name = input('Введите имя вашего будущего питомца\nДалее у вас будет возможность выбрать его!'
                         '\nИмя питомца: ')

        pet = Pet(pet_name)

        print(Animal.TYPE_OF_PET)

        while True:
            a = input()
            if a == '1':
                pet.set_type(Type.type_pet[1])
                print(Animal.CAT)
                break
            elif a == '2':
                pet.set_type(Type.type_pet[2])
                print(Animal.DOG)
                break
            else:
                print('Неправильный выбор, попробуйте еще раз!')

        print(f'Теперь это Ваш питомец!'
              f'\nЗаботьтесь о {pet.name} как о настоящем любимце.')

        coins = 15
        reg = RegistrationPolicy()
        reg.registration(name, password)

        self.user = User(name, password, pet, coins, {})
        JSON.register_json(self.user.name, password, pet.to_dict(), coins)

        print(RULES)

        print(CONTINEU_QUESTION)
        question = input('Ввод: ')
        if question == '1':
            self.response()
        else:
            sys.exit(1)

    def response(self):
        print(OPTIONS_TODO)

        while True:
            user_input = input('Выберите команду: ')
            if user_input == '1':
                print(RULES)
                print(OPTIONS_TODO)
            if user_input == '2':
                self.add_task()
            if user_input == '3':
                self.user.todo.print_only_index_and_name()
                self.response()
            if user_input == '4':
                self.edit_task()
            if user_input == '5':
                self.user.todo.sort_by_status()
                print(OPTIONS_TODO)
            if user_input == '6':
                self.user.todo.sort_by_category()
                print(OPTIONS_TODO)
            if user_input == '7':
                self.info_pet()
            if user_input == '8':
                self.buy_item()
            if user_input == '9':
                self.feed_pet()
            if user_input == '0':
                sys.exit(1)

    def add_task(self):
        print('Давайте добавим новую задачу.')
        user_input = input('Задача: ')

        new_task = Task()
        new_task.set_title(user_input)

        new_date = datetime.date.today()
        new_task.set_date_of_created(new_date)

        self.user.todo.add_to_do(new_task)
        print('Новая задача "', new_task.name, '" была добавлена!')

        users = JSON.load_from_json()

        list_ = [new_task.to_dict()]
        users[self.user.name]['todo_task'] += list_

        JSON.dump_to_json(users)

        print(OPTIONS_TODO)

    def edit_task(self):
        print(OPTIONS_EDIT_TASK)

        user_input = input()

        if user_input == '0':
            self.response()
        elif user_input == '1':
            self.remove_task()
        elif user_input == '2':
            self.edit_status()
        elif user_input == '3':
            self.update()
        else:
            print('Неправильный выбор, попробуйте еще раз!')
            print(OPTIONS_TODO)

    def remove_task(self):
        self.user.todo.print_only_index_and_name()

        if len(self.user.todo.get_to_do_list()) != 0:
            print('Хотите удалить что-то из списка задач?')

            while True:
                user_input = input('Введите номер задачи: ')

                remove_by_number = int(user_input)
                if remove_by_number != 0:
                    self.user.todo.remove_to_do(remove_by_number - 1)
                    users = JSON.load_from_json()

                    list_ = users[self.user.name]['todo_task']
                    del list_[remove_by_number - 1]
                    users[self.user.name]['todo_task'] = list_

                    JSON.dump_to_json(users)

                    print(OPTIONS_TODO)
                    break
                else:
                    print(OPTIONS_TODO)
                    self.response()
        else:
            print('Ваш список пуст! Удалять нечего.')
            self.response()

    def edit_status(self):
        print('Успели что-то сделать? Давайте отметим это.')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Введите номер задачи: ')

                get_task_by_name = int(user_input)
                if get_task_by_name != 0:
                    searched = self.user.todo.task_in_to_do(get_task_by_name - 1)
                    print(searched.status)

                    if searched.status != Status.DONE:
                        users = JSON.load_from_json()

                        list_ = users[self.user.name]['todo_task']

                        for i in range(len(list_)):
                            if i == get_task_by_name - 1:
                                list_[i]['status'] = Status.DONE.name

                        users[self.user.name]['coins'] += 15

                        print(OPTIONS_TODO)
                        JSON.dump_to_json(users)

                        break
                    else:
                        print('Эта задачу уже сделана.')
                        break
                else:
                    print(OPTIONS_TODO)
                    self.response()

            if searched.status != Status.DONE:
                searched.set_status(Status.DONE)
                print('Задание готово! Вы молодец.')
        else:
            print('Нет задач в списке!')
            self.response()

    def update(self):
        print(OPTIONS_UPDATE)

        user_input = input()

        if user_input == '0':
            print(OPTIONS_TODO)
            self.response()
        elif user_input == '1':
            self.edit_name()
        elif user_input == '2':
            self.edit_category()
        else:
            print('Неправильный выбор, попробуйте еще раз!')
            print(OPTIONS_TODO)

    def edit_name(self):
        print('Вы можете изменить имя задачи.')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Введите номер задачи: ')

                get_title_by_number = int(user_input)
                if get_title_by_number != 0:
                    searched = self.user.todo.task_in_to_do(get_title_by_number - 1)
                    break
                else:
                    print(OPTIONS_TODO)
                    self.response()

            new_name = input('Введите новое имя задачи: ')

            users = JSON.load_from_json()

            list_ = users[self.user.name]['todo_task']

            for i in range(len(list_)):
                if i == get_title_by_number - 1:
                    list_[i]['name'] = new_name

            JSON.dump_to_json(users)

            searched.set_title(new_name)
            print('Новое имя задачи: ', searched.get_title())
            print(OPTIONS_TODO)
        else:
            print('Ваш список задач пуст!')
            print(OPTIONS_TODO)
            self.response()

    def edit_category(self):
        print('Желаете изменить категорию задачи?')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Введите номер задачи: ')

                get_task_by_name = int(user_input)
                if get_task_by_name != 0:
                    searched = self.user.todo.task_in_to_do(get_task_by_name - 1)
                    break
                else:
                    print(OPTIONS_TODO)
                    self.response()

            print(CATEGORY)
            category = input('Введите номер категории: ')

            if category == '1':
                searched.set_category(Category.NONE)
                users = JSON.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.NONE.name

                JSON.dump_to_json(users)

            if category == '2':
                searched.set_category(Category.LEARNING)
                users = JSON.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.LEARNING.name

                JSON.dump_to_json(users)

            if category == '3':
                searched.set_category(Category.WORKING)
                users = JSON.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.WORKING.name

                JSON.dump_to_json(users)

            if category == '4':
                searched.set_category(Category.PERSONAL)
                users = JSON.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.PERSONAL.name

                JSON.dump_to_json(users)

            if category == '5':
                searched.set_category(Category.TRAVELING)
                users = JSON.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.TRAVELING.name

                JSON.dump_to_json(users)

            if category == '6':
                searched.set_category(Category.DAILY)
                users = JSON.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.DAILY.name

                JSON.dump_to_json(users)

            print('Категория была изменена.')
            print(OPTIONS_TODO)
        else:
            print('Ваш список задач пуст!')
            print(OPTIONS_TODO)
            self.response()

    def buy_item(self):
        store = Storage()

        print('Добро пожаловать в магазин!'
              '\nЗдесь Вы можете купить продукты для своего питомца.')
        print(store.get_items())

        Products.buy_json(self.user)

    def info_pet(self):
        self.check()
        users = JSON.load_from_json()

        pet_ = users[self.user.name]['pet']

        if pet_['type'] == Type.type_pet[1]:
            print(f'Имя: {pet_["name"]}'
                  f'\nТип: {pet_["type"]}'
                  f'\n{Animal.CAT}'
                  f'\nНастроение: {pet_["happiness"]}')
        if pet_['type'] == Type.type_pet[2]:
            print(f'Имя: {pet_["name"]}'
                  f'\nТип: {pet_["type"]}'
                  f'\n{Animal.DOG}'
                  f'\nНастроение: {pet_["happiness"]}')

        self.response()

    def info_about_pet(self):
        users = JSON.load_from_json()

        pet_file = users[self.user.name]['pet']

        name = pet_file['name']
        type = pet_file['type']
        mood = pet_file['happiness']
        date = pet_file['date']

        pet_ = Pet(name)

        pet_.set_type(type)
        pet_.set_mood(mood)
        pet_.set_age(datetime.datetime.strptime(date, '%Y-%m-%d').date())

        return pet_

    def check(self):
        pet_ = self.info_about_pet()

        mood = pet_.check_mood()

        users = JSON.load_from_json()

        dict_ = users[self.user.name]['pet']

        dict_['happiness'] = mood
        dict_['date'] = datetime.date.today().isoformat()

        JSON.dump_to_json(users)

    def feed_pet(self):
        self.check()
        pet_ = self.info_about_pet()

        print(QUESTION_FOOD)

        choice = input()
        if choice == '1':
            users = JSON.load_from_json()

            dict_ = users[self.user.name]['items']
            pet_file = users[self.user.name]['pet']

            print(f'Ваш инвентарь: {dict_}')

            if dict_['FISH'] == 0 and dict_['BONE'] == 0:
                print('К сожалению, в Вашем инвентаре ничего нет!')
                self.response()

            print('1. Рыбка (FISH),'
                  '\n2. Косточка (BONE),'
                  '\n3. Выход')

            while True:
                food = input()
                if food == '1':
                    food = TYPE_ITEM[0]

                    mood_ = pet_.feed(food)
                    self.user.pet['happiness'] = mood_
                    pet_file['happiness'] = mood_
                    dict_['FISH'] -= 1

                elif food == '2':
                    food = TYPE_ITEM[1]

                    mood_ = pet_.feed(food)
                    self.user.pet['happiness'] = mood_
                    pet_file['happiness'] = mood_
                    dict_['BONE'] -= 1

                elif food == '3':
                    break
                else:
                    print('Неправильный выбор, попробуйте еще раз!')

            JSON.dump_to_json(users)
            self.response()

        if choice == '2':
            self.response()


class ApplicationBIN:

    def run(self):
        users = BIN.load_from_bin()

        for name in users:
            print(f'Пользователь: {name}')

        print(QUESTION)

        while True:
            choice = input()

            if choice == '1':
                self.login()
                break
            elif choice == '2':
                self.register()
                break
            else:
                print('Неправильный выбор, попробуйте еще раз!')

    def login(self):
        name = input('Введите имя: ')
        password = input('Введите пароль: ')

        users = BIN.load_from_bin()

        if name not in users:
            print(PROBLEM)
            self.run()

        if name in users and users[name]['password'] == password:
            coins = users[name]['coins']
            items = users[name]['items']
            pet = users[name]['pet']

            self.user = User(name, password, pet, coins, items)
            list_ = users[name]['todo_task']

            print(coins)

            for i in list_:
                task = Task()
                task.set_title(i['name'])

                if i['status'] == Status.DONE.name:
                    task.set_status(Status.DONE)
                else:
                    task.set_status(Status.PENDING)
                if i['category'] == Category.NONE.name:
                    task.set_category(Category.NONE)
                elif i['category'] == Category.DAILY.name:
                    task.set_category(Category.DAILY)
                elif i['category'] == Category.WORKING.name:
                    task.set_category(Category.WORKING)
                elif i['category'] == Category.LEARNING.name:
                    task.set_category(Category.LEARNING)
                elif i['category'] == Category.TRAVELING.name:
                    task.set_category(Category.TRAVELING)
                else:
                    task.set_category(Category.PERSONAL)

                task.set_date_of_created(i['creation_time'])
                task.set_price(i['price'])

                self.user.todo.add_to_do(task)

        elif name in users and users[name]['password'] != password:
            print('Вы ввели неправильный пароль :(\nПопробуйте еще раз!')
            self.login()

        self.response()

    def register(self):
        name = input('Введите имя: ')

        users = BIN.load_from_bin()

        if name in users:
            print('Такое имя пользователя уже существует :(\n'
                  'Попробуйте ввести другое имя для регистрации')
            self.register()

        password = input('Введите пароль: ')
        pet_name = input('Введите имя вашего будущего питомца\nДалее у вас будет возможность выбрать его!'
                         '\nИмя питомца: ')

        pet = Pet(pet_name)

        print(Animal.TYPE_OF_PET)

        while True:
            a = input()
            if a == '1':
                pet.set_type(Type.type_pet[1])
                print(Animal.CAT)
                break
            elif a == '2':
                pet.set_type(Type.type_pet[2])
                print(Animal.DOG)
                break
            else:
                print('Неправильный выбор, попробуйте еще раз!')

        print(f'Теперь это Ваш питомец!'
              f'\nЗаботьтесь о {pet.name} как о настоящем любимце.')

        coins = 15
        self.user = User(name, password, pet, coins, {})
        BIN.register_bin(self.user.name, password, pet.to_dict(), coins)

        print(RULES)

        print(CONTINEU_QUESTION)
        question = input('Ввод: ')
        if question == '1':
            self.response()
        else:
            sys.exit(1)

    def response(self):
        print(OPTIONS_TODO)

        while True:
            user_input = input('Выберите команду: ')
            if user_input == '1':
                print(RULES)
                print(OPTIONS_TODO)
            if user_input == '2':
                self.add_task()
            if user_input == '3':
                self.user.todo.print_only_index_and_name()
                self.response()
            if user_input == '4':
                self.edit_task()
            if user_input == '5':
                self.user.todo.sort_by_status()
                print(OPTIONS_TODO)
            if user_input == '6':
                self.user.todo.sort_by_category()
                print(OPTIONS_TODO)
            if user_input == '7':
                self.info_pet()
            if user_input == '8':
                self.buy_item()
            if user_input == '9':
                self.feed_pet()
            if user_input == '0':
                sys.exit(1)

    def add_task(self):
        print('Давайте добавим новую задачу.')
        user_input = input('Задача: ')

        new_task = Task()
        new_task.set_title(user_input)

        new_date = datetime.date.today()
        new_task.set_date_of_created(new_date)

        self.user.todo.add_to_do(new_task)
        print('Новая задача "', new_task.name, '" была добавлена!')

        users = BIN.load_from_bin()

        list_ = [new_task.to_dict()]
        users[self.user.name]['todo_task'] += list_

        BIN.dump_to_bin(users)

        print(OPTIONS_TODO)

    def edit_task(self):
        print(OPTIONS_EDIT_TASK)

        user_input = input()

        if user_input == '0':
            self.response()
        elif user_input == '1':
            self.remove_task()
        elif user_input == '2':
            self.edit_status()
        elif user_input == '3':
            self.update()
        else:
            print('Неправильный выбор, попробуйте еще раз!')
            print(OPTIONS_TODO)

    def remove_task(self):
        self.user.todo.print_only_index_and_name()

        if len(self.user.todo.get_to_do_list()) != 0:
            print('Хотите удалить что-то из списка задач?')

            while True:
                user_input = input('Введите номер задачи: ')

                remove_by_number = int(user_input)
                if remove_by_number != 0:
                    self.user.todo.remove_to_do(remove_by_number - 1)
                    users = BIN.load_from_bin()

                    list_ = users[self.user.name]['todo_task']
                    del list_[remove_by_number - 1]
                    users[self.user.name]['todo_task'] = list_

                    BIN.dump_to_bin(users)

                    print(OPTIONS_TODO)
                    break
                else:
                    print(OPTIONS_TODO)
                    self.response()
        else:
            print('Ваш список пуст! Удалять нечего.')
            print(OPTIONS_TODO)
            self.response()

    def edit_status(self):
        print('Успели что-то сделать? Давайте отметим это.')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Введите номер задачи: ')

                get_task_by_name = int(user_input)
                if get_task_by_name != 0:
                    searched = self.user.todo.task_in_to_do(get_task_by_name - 1)
                    print(searched.status)

                    if searched.status != Status.DONE:
                        users = BIN.load_from_bin()

                        list_ = users[self.user.name]['todo_task']

                        for i in range(len(list_)):
                            if i == get_task_by_name - 1:
                                list_[i]['status'] = Status.DONE.name

                        users[self.user.name]['coins'] += 15

                        BIN.dump_to_bin(users)

                        print(OPTIONS_TODO)
                        break
                    else:
                        print('Эта задачу уже сделана.')
                        break
                else:
                    print(OPTIONS_TODO)
                    self.response()

            if searched.status != Status.DONE:
                searched.set_status(Status.DONE)
                print('Задание готово! Вы молодец.')
        else:
            print('Нет задач в списке!')
            print(OPTIONS_TODO)
            self.response()

    def update(self):
        print(OPTIONS_UPDATE)

        user_input = input()

        if user_input == '0':
            print(OPTIONS_TODO)
            self.response()
        elif user_input == '1':
            self.edit_name()
        elif user_input == '2':
            self.edit_category()
        else:
            print('Неправильный выбор, попробуйте еще раз!')
            print(OPTIONS_TODO)

    def edit_name(self):
        print('Вы можете изменить имя задачи.')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Выберите номер задачи: ')

                get_title_by_number = int(user_input)
                if get_title_by_number != 0:
                    searched = self.user.todo.task_in_to_do(get_title_by_number - 1)
                    break
                else:
                    print(OPTIONS_TODO)
                    self.response()

            new_name = input('Выберите новое имя задачи: ')

            users = BIN.load_from_bin()

            list_ = users[self.user.name]['todo_task']

            for i in range(len(list_)):
                if i == get_title_by_number - 1:
                    list_[i]['name'] = new_name

            BIN.dump_to_bin(users)

            searched.set_title(new_name)
            print('Новое имя задачи: ', searched.get_title())
        else:
            print('Ваш список задач пуст!')
            print(OPTIONS_TODO)
            self.response()

    def edit_category(self):
        print('Желаете изменить категорию задачи?')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Введите номер задачи: ')

                get_task_by_name = int(user_input)
                if get_task_by_name != 0:
                    searched = self.user.todo.task_in_to_do(get_task_by_name - 1)
                    break
                else:
                    print(OPTIONS_TODO)
                    self.response()

            print(CATEGORY)
            category = input('Введите номер категории: ')

            if category == '1':
                searched.set_category(Category.NONE)
                users = BIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.NONE.name

                BIN.dump_to_bin(users)

            if category == '2':
                searched.set_category(Category.LEARNING)
                users = BIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.LEARNING.name

                BIN.dump_to_bin(users)

            if category == '3':
                searched.set_category(Category.WORKING)
                users = BIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.WORKING.name

                BIN.dump_to_bin(users)

            if category == '4':
                searched.set_category(Category.PERSONAL)
                users = BIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.PERSONAL.name

                BIN.dump_to_bin(users)

            if category == '5':
                searched.set_category(Category.TRAVELING)
                users = BIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.TRAVELING.name

                BIN.dump_to_bin(users)

            if category == '6':
                searched.set_category(Category.DAILY)
                users = BIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.DAILY.name

                BIN.dump_to_bin(users)

            print('Категория была изменена.')
        else:
            print('Ваш список задач пуст!')
            print(OPTIONS_TODO)
            self.response()

    def buy_item(self):
        store = Storage()

        print('Добро пожаловать в магазин!'
              '\nЗдесь Вы можете купить продукты для своего питомца.')
        print(store.get_items())

        Products.buy_bin(self.user)

    def info_pet(self):
        self.check()
        users = BIN.load_from_bin()

        pet_ = users[self.user.name]['pet']

        if pet_['type'] == Type.type_pet[1]:
            print(f'Имя: {pet_["name"]}'
                  f'\nТип: {pet_["type"]}'
                  f'\n{Animal.CAT}'
                  f'\nНастроение: {pet_["happiness"]}')
        if pet_['type'] == Type.type_pet[2]:
            print(f'Имя: {pet_["name"]}'
                  f'\nТип: {pet_["type"]}'
                  f'\n{Animal.DOG}'
                  f'\nНастроение: {pet_["happiness"]}')

        self.response()

    def info_about_pet(self):
        users = BIN.load_from_bin()

        pet_file = users[self.user.name]['pet']

        name = pet_file['name']
        type = pet_file['type']
        mood = pet_file['happiness']
        date = pet_file['date']

        pet_ = Pet(name)

        pet_.set_type(type)
        pet_.set_mood(mood)
        pet_.set_age(datetime.datetime.strptime(date, '%Y-%m-%d').date())

        return pet_

    def check(self):
        pet_ = self.info_about_pet()

        mood = pet_.check_mood()

        users = BIN.load_from_bin()

        dict_ = users[self.user.name]['pet']

        dict_['happiness'] = mood
        dict_['date'] = datetime.date.today().isoformat()

        BIN.dump_to_bin(users)

    def feed_pet(self):
        self.check()
        pet_ = self.info_about_pet()

        print(QUESTION_FOOD)

        choice = input()
        if choice == '1':
            users = BIN.load_from_bin()

            dict_ = users[self.user.name]['items']
            pet_file = users[self.user.name]['pet']

            print(f'Ваш инвентарь: {dict_}')

            if dict_['FISH'] == 0 and dict_['BONE'] == 0:
                print('К сожалению, в Вашем инвентаре ничего нет!')
                self.response()

            print('1. Рыбка (FISH),'
                  '\n2. Косточка (BONE),'
                  '\n3. Выход')

            while True:
                food = input()
                if food == '1':
                    food = TYPE_ITEM[0]

                    mood_ = pet_.feed(food)
                    self.user.pet['happiness'] = mood_
                    pet_file['happiness'] = mood_
                    dict_['FISH'] -= 1

                elif food == '2':
                    food = TYPE_ITEM[1]

                    mood_ = pet_.feed(food)
                    self.user.pet['happiness'] = mood_
                    pet_file['happiness'] = mood_
                    dict_['BONE'] -= 1

                elif food == '3':
                    break
                else:
                    print('Неправильный выбор, попробуйте еще раз!')

            BIN.dump_to_bin(users)
            self.response()

        if choice == '2':
            self.response()

if __name__ == "__main__":
    app = ApplicationJSON()
    app.run()
