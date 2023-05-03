import constants
from task import Task, Status, Category
from user import User
import datetime
import json
import os
import pickle
from registrationpolicy import RegistrationPolicy
from animal import Type
from pet import Pet
from storage import Storage
from products import Products

import sys
import des
from PyQt5 import QtWidgets


class ApplicationJSON:

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
        users = self.load_from_json()

        for name in users:
            print(f'User: {name}')

        print('What are you want to do?'
              '\n1 - logging'
              '\n2 - registration')

        while True:
            choice = input()

            if choice == '1':
                self.login()
                break
            elif choice == '2':
                self.register()
                break
            else:
                print('Invalid choice, try again')

    def login(self):
        name = input('Enter your name: ')
        password = input('Enter your password: ')

        users = self.load_from_json()

        if name not in users:
            print('You are not user! Try register!')
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
            print('Password is wrong! Try again!')
            self.login()

        self.response()

    def register(self):
        name = input('Enter your name: ')

        users = self.load_from_json()

        if name in users:
            print('This name is not available! Please, choose other name')
            self.register()

        password = input('Enter your password: ')
        pet_name = input('Enter name of your pet: ')
        pet = Pet(pet_name)

        print('Choose a type of your pet!'
              '\n1 - Cat'
              '\n2 - Dog')

        while True:
            a = input()
            if a == '1':
                pet.set_type(Type.type_pet[1])
                break
            elif a == '2':
                pet.set_type(Type.type_pet[2])
                break
            else:
                print('Invalid choice, try again')

        coins = 15
        self.user = User(name, password, pet, coins, {})
        RegistrationPolicy.register_json(self.user.name, password, pet.to_dict(), coins)
        self.response()

    def response(self):
        print(constants.OPTIONS_TODO)

        while True:
            user_input = input('Choose command: ')
            if user_input == '1':
                self.add_task()
            if user_input == '2':
                self.edit_task()
            if user_input == '3':
                self.user.todo.sort_by_status()
            if user_input == '4':
                self.user.todo.sort_by_category()
            if user_input == '5':
                self.buy_item()
            if user_input == '6':
                self.info_pet()
            if user_input == '7':
                self.feed_pet()

    def add_task(self):
        print('ADD NEW TASK!')
        user_input = input('Name of task: ')

        new_task = Task()
        new_task.set_title(user_input)

        new_date = datetime.date.today()
        new_task.set_date_of_created(new_date)

        self.user.todo.add_to_do(new_task)
        print('New task "', new_task.name, '" was added!')

        users = self.load_from_json()

        list_ = [new_task.to_dict()]
        users[self.user.name]['todo_task'] += list_

        self.dump_to_json(users)

    def edit_task(self):
        print(constants.OPTIONS_EDIT_TASK)
        user_input = input()

        if user_input == '0':
            self.response()
        elif user_input == '1':
            self.remove_task()
        elif user_input == '2':
            self.edit_status()
        elif user_input == '3':
            self.update()
        elif user_input == '4':
            self.user.todo.sort_by_status()

    def remove_task(self):
        self.user.todo.print_only_index_and_name()

        if len(self.user.todo.get_to_do_list()) != 0:
            print('Do you want delete something?')

            while True:
                user_input = input('Enter the number of the task!')

                remove_by_number = int(user_input)
                if remove_by_number != 0:
                    self.user.todo.remove_to_do(remove_by_number - 1)
                    users = self.load_from_json()

                    list_ = users[self.user.name]['todo_task']
                    del list_[remove_by_number - 1]
                    users[self.user.name]['todo_task'] = list_

                    self.dump_to_json(users)

                    break
                else:
                    self.response()
        else:
            print('No task for remove!')
            self.response()

    def edit_status(self):
        print('Done something? Mark it!')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Enter the number of the task!')

                get_task_by_name = int(user_input)
                if get_task_by_name != 0:
                    searched = self.user.todo.task_in_to_do(get_task_by_name - 1)
                    print(searched.status)

                    if searched.status != Status.DONE:
                        users = self.load_from_json()

                        list_ = users[self.user.name]['todo_task']

                        for i in range(len(list_)):
                            if i == get_task_by_name - 1:
                                list_[i]['status'] = Status.DONE.name

                        users[self.user.name]['coins'] += 15

                        self.dump_to_json(users)

                        break
                    else:
                        print('This task is already done!')
                        break
                else:
                    self.response()

            if searched.status != Status.DONE:
                searched.set_status(Status.DONE)
                print('TASK DONE! GRATEFUL!')
        else:
            print('No task in todo!')
            self.response()

    def update(self):
        print(constants.OPTIONS_UPDATE)

        user_input = input()

        if user_input == '0':
            self.response()
        elif user_input == '1':
            self.edit_name()
        elif user_input == '2':
            self.edit_category()

    def edit_name(self):
        print('You can edit name of task now!')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input()

                get_title_by_number = int(user_input)
                if get_title_by_number != 0:
                    searched = self.user.todo.task_in_to_do(get_title_by_number - 1)
                    break
                else:
                    self.response()

            new_name = input('Enter new name of the task: ')

            users = self.load_from_json()

            list_ = users[self.user.name]['todo_task']

            for i in range(len(list_)):
                if i == get_title_by_number - 1:
                    list_[i]['name'] = new_name

            self.dump_to_json(users)

            searched.set_title(new_name)
            print('New name of the task: ', searched.get_title())
        else:
            print('No task in todo!')
            self.response()

    def edit_category(self):
        print('Need some category? Do it!')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Enter the number of the task!')

                get_task_by_name = int(user_input)
                if get_task_by_name != 0:
                    searched = self.user.todo.task_in_to_do(get_task_by_name - 1)
                    break
                else:
                    self.response()

            print(constants.CATEGORY)
            category = input('Enter the numer of category: ')

            if category == '1':
                searched.set_category(Category.NONE)
                users = self.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.NONE.name

                self.dump_to_json(users)

            if category == '2':
                searched.set_category(Category.LEARNING)
                users = self.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.LEARNING.name

                self.dump_to_json(users)

            if category == '3':
                searched.set_category(Category.WORKING)
                users = self.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.WORKING.name

                self.dump_to_json(users)

            if category == '4':
                searched.set_category(Category.PERSONAL)
                users = self.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.PERSONAL.name

                self.dump_to_json(users)

            if category == '5':
                searched.set_category(Category.TRAVELING)
                users = self.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.TRAVELING.name

                self.dump_to_json(users)

            if category == '6':
                searched.set_category(Category.DAILY)
                users = self.load_from_json()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.DAILY.name

                self.dump_to_json(users)

            print('Category was changed!')
        else:
            print('No task in todo!')
            self.response()

    def buy_item(self):
        store = Storage()

        print('Welcome to store! Buy some items if you need!')
        print(store.get_items())

        Products.buy_json(self.user)

    def info_pet(self):
        self.check()
        users = self.load_from_json()

        pet_ = users[self.user.name]['pet']

        print(f'NAME: {pet_["name"]}'
              f'\nTYPE: {pet_["type"]}'
              f'\nHAPPINESS: {pet_["happiness"]}')

    def info_about_pet(self):
        name = self.user.pet['name']
        type = self.user.pet['type']
        mood = self.user.pet['happiness']
        date = self.user.pet['date']

        pet_ = Pet(name)

        pet_.set_type(type)
        pet_.set_mood(mood)
        pet_.set_age(datetime.datetime.strptime(date, '%Y-%m-%d').date())

        return pet_

    def check(self):
        pet_ = self.info_about_pet()

        mood = pet_.check_mood()

        users = self.load_from_json()

        dict_ = users[self.user.name]['pet']

        dict_['happiness'] = mood
        dict_['date'] = datetime.date.today().isoformat()

        self.dump_to_json(users)

    def feed_pet(self):
        pet_ = self.info_about_pet()

        print('Do you want to feed your pet?'
              '\n1. Yes!'
              '\n2. No...')

        choice = input()
        if choice == '1':
            users = self.load_from_json()

            dict_ = users[self.user.name]['items']
            pet_file = users[self.user.name]['pet']

            print(f'Your inventory: {dict_}')

            print('1. Fish,'
                  '\n2. Bone,'
                  '\n3. Exit')

            while True:
                food = input()
                if food == '1':
                    food = 'FISH'

                    mood_ = pet_.feed(food)
                    self.user.pet['happiness'] = mood_
                    pet_file['happiness'] = mood_
                    dict_['FISH'] -= 1

                    print(f'Your pay: {food} - 15c')

                elif food == '2':
                    food = 'BONE'

                    mood_ = pet_.feed(food)
                    self.user.pet['happiness'] = mood_
                    pet_file['happiness'] = mood_
                    dict_['BONE'] -= 1

                    print(f'Your pay: {food} - 15c')

                elif food == '3':
                    break
                else:
                    print('Invalid choice, try again!')

            self.dump_to_json(users)


class ApplicationBIN:
    @staticmethod
    def load_from_bin():
        with open('users.bin', 'rb') as file:
            if os.path.getsize('users.bin') != 0:
                users = pickle.load(file)
            else:
                users = {}

        return users

    @staticmethod
    def dump_to_bin(users):
        with open('users.bin', 'wb') as f:
            pickle.dump(users, f, protocol=3)

    def run(self):
        users = ApplicationBIN.load_from_bin()

        for name in users:
            print(f'User: {name}')

        print('What are you want to do?'
              '\n1 - logging'
              '\n2 - registration')

        while True:
            choice = input()

            if choice == '1':
                self.login()
                break
            elif choice == '2':
                self.register()
                break
            else:
                print('Invalid choice, try again')

    def login(self):
        name = input('Enter your name: ')
        password = input('Enter your password: ')

        users = ApplicationBIN.load_from_bin()

        if name not in users:
            print('You are not user! Try register!')
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
            print('Password is wrong! Try again!')
            self.login()

        self.response()

    def register(self):
        name = input('Enter your name: ')

        users = ApplicationBIN.load_from_bin()

        if name in users:
            print('This name is not available! Please, choose other name')
            self.register()

        password = input('Enter your password: ')
        pet_name = input('Enter name of your pet: ')
        pet = Pet(pet_name)

        print('Choose a type of your pet!'
              '\n1 - Cat'
              '\n2 - Dog')

        while True:
            a = input()
            if a == '1':
                pet.set_type(Type.type_pet[1])
                break
            elif a == '2':
                pet.set_type(Type.type_pet[2])
                break
            else:
                print('Invalid choice, try again')

        coins = 15
        self.user = User(name, password, pet, coins, {})
        RegistrationPolicy.register_bin(self.user.name, password, pet.to_dict(), coins)
        self.response()

    def response(self):
        print(constants.OPTIONS_TODO)

        while True:
            user_input = input('Choose command: ')
            if user_input == '1':
                self.add_task()
            if user_input == '2':
                self.edit_task()
            if user_input == '3':
                self.user.todo.sort_by_status()
            if user_input == '4':
                self.user.todo.sort_by_category()
            if user_input == '5':
                self.buy_item()
            if user_input == '6':
                self.info_pet()
            if user_input == '7':
                self.feed_pet()

    def add_task(self):
        print('ADD NEW TASK!')
        user_input = input('Name of task: ')

        new_task = Task()
        new_task.set_title(user_input)

        new_date = datetime.date.today()
        new_task.set_date_of_created(new_date)

        self.user.todo.add_to_do(new_task)
        print('New task "', new_task.name, '" was added!')

        users = ApplicationBIN.load_from_bin()

        list_ = [new_task.to_dict()]
        users[self.user.name]['todo_task'] += list_

        ApplicationBIN.dump_to_bin(users)

    def edit_task(self):
        print(constants.OPTIONS_EDIT_TASK)
        user_input = input()

        if user_input == '0':
            self.response()
        elif user_input == '1':
            self.remove_task()
        elif user_input == '2':
            self.edit_status()
        elif user_input == '3':
            self.update()
        elif user_input == '4':
            self.user.todo.sort_by_status()

    def remove_task(self):
        self.user.todo.print_only_index_and_name()

        if len(self.user.todo.get_to_do_list()) != 0:
            print('Do you want delete something?')

            while True:
                user_input = input('Enter the number of the task!')

                remove_by_number = int(user_input)
                if remove_by_number != 0:
                    self.user.todo.remove_to_do(remove_by_number - 1)
                    users = ApplicationBIN.load_from_bin()

                    list_ = users[self.user.name]['todo_task']
                    del list_[remove_by_number - 1]
                    users[self.user.name]['todo_task'] = list_

                    ApplicationBIN.dump_to_bin(users)
                    break
                else:
                    self.response()
        else:
            print('No task for remove!')
            self.response()

    def edit_status(self):
        print('Done something? Mark it!')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Enter the number of the task!')

                get_task_by_name = int(user_input)
                if get_task_by_name != 0:
                    searched = self.user.todo.task_in_to_do(get_task_by_name - 1)
                    print(searched.status)

                    if searched.status != Status.DONE:
                        users = ApplicationBIN.load_from_bin()

                        list_ = users[self.user.name]['todo_task']

                        for i in range(len(list_)):
                            if i == get_task_by_name - 1:
                                list_[i]['status'] = Status.DONE.name

                        users[self.user.name]['coins'] += 15

                        ApplicationBIN.dump_to_bin(users)
                        break
                    else:
                        print('This task is already done!')
                        break
                else:
                    self.response()

            if searched.status != Status.DONE:
                searched.set_status(Status.DONE)
                print('TASK DONE! GRATEFUL!')
        else:
            print('No task in todo!')
            self.response()

    def update(self):
        print(constants.OPTIONS_UPDATE)

        user_input = input()

        if user_input == '0':
            self.response()
        elif user_input == '1':
            self.edit_name()
        elif user_input == '2':
            self.edit_category()

    def edit_name(self):
        print('You can edit name of task now!')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input()

                get_title_by_number = int(user_input)
                if get_title_by_number != 0:
                    searched = self.user.todo.task_in_to_do(get_title_by_number - 1)
                    break
                else:
                    self.response()

            new_name = input('Enter new name of the task: ')

            users = ApplicationBIN.load_from_bin()

            list_ = users[self.user.name]['todo_task']

            for i in range(len(list_)):
                if i == get_title_by_number - 1:
                    list_[i]['name'] = new_name

            ApplicationBIN.dump_to_bin(users)

            searched.set_title(new_name)
            print('New name of the task: ', searched.get_title())
        else:
            print('No task in todo!')
            self.response()

    def edit_category(self):
        print('Need some category? Do it!')
        self.user.todo.print_only_index_and_name()

        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            while True:
                user_input = input('Enter the number of the task!')

                get_task_by_name = int(user_input)
                if get_task_by_name != 0:
                    searched = self.user.todo.task_in_to_do(get_task_by_name - 1)
                    break
                else:
                    self.response()

            print(constants.CATEGORY)
            category = input('Enter the numer of category: ')

            if category == '1':
                searched.set_category(Category.NONE)
                users = ApplicationBIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.NONE.name

                ApplicationBIN.dump_to_bin(users)

            if category == '2':
                searched.set_category(Category.LEARNING)
                users = ApplicationBIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.LEARNING.name

                ApplicationBIN.dump_to_bin(users)

            if category == '3':
                searched.set_category(Category.WORKING)
                users = ApplicationBIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.WORKING.name

                ApplicationBIN.dump_to_bin(users)

            if category == '4':
                searched.set_category(Category.PERSONAL)
                users = ApplicationBIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.PERSONAL.name

                ApplicationBIN.dump_to_bin(users)

            if category == '5':
                searched.set_category(Category.TRAVELING)
                users = ApplicationBIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.TRAVELING.name

                ApplicationBIN.dump_to_bin(users)

            if category == '6':
                searched.set_category(Category.DAILY)
                users = ApplicationBIN.load_from_bin()

                list_ = users[self.user.name]['todo_task']

                for i in range(len(list_)):
                    if i == get_task_by_name - 1:
                        list_[i]['category'] = Category.DAILY.name

                ApplicationBIN.dump_to_bin(users)

            print('Category was changed!')
        else:
            print('No task in todo!')
            self.response()

    def buy_item(self):
        store = Storage()

        print('Welcome to store! Buy some items if you need!')
        print(store.get_items())

        Products.buy_bin(self.user)

    def info_pet(self):
        self.check()
        users = ApplicationBIN.load_from_bin()

        pet_ = users[self.user.name]['pet']

        print(f'NAME: {pet_["name"]}'
              f'\nTYPE: {pet_["type"]}'
              f'\nHAPPINESS: {pet_["happiness"]}')

    def check(self):
        name = self.user.pet['name']
        type = self.user.pet['type']
        mood = self.user.pet['happiness']
        date = self.user.pet['date']

        pet_ = Pet(name)

        pet_.set_type(type)
        pet_.set_mood(mood)
        pet_.set_age(datetime.datetime.strptime(date, '%Y-%m-%d').date())

        mood = pet_.check_mood()

        users = ApplicationBIN.load_from_bin()

        dict_ = users[self.user.name]['pet']

        dict_['happiness'] = mood
        dict_['date'] = datetime.date.today().isoformat()

        ApplicationBIN.dump_to_bin(users)

    def feed_pet(self):
        name = self.user.pet['name']
        type = self.user.pet['type']
        mood = self.user.pet['happiness']
        date = self.user.pet['date']

        pet_ = Pet(name)

        pet_.set_type(type)
        pet_.set_mood(mood)
        pet_.set_age(datetime.datetime.strptime(date, '%Y-%m-%d').date())

        print('Do you want to feed your pet?'
              '\n1. Yes!'
              '\n2. No...')

        choice = input()
        if choice == '1':
            users = ApplicationBIN.load_from_bin()

            dict_ = users[self.user.name]['items']
            pet_file = users[self.user.name]['pet']

            print(f'Your inventory: {dict_}')

            print('1. Fish,'
                  '\n2. Bone,'
                  '\n3. Exit')

            while True:
                food = input()
                if food == '1':
                    food = 'FISH'

                    mood_ = pet_.feed(food)
                    self.user.pet['happiness'] = mood_
                    pet_file['happiness'] = mood_
                    dict_['FISH'] -= 1

                    print(f'Your pay: {food} - 15c')

                elif food == '2':
                    food = 'BONE'

                    mood_ = pet_.feed(food)
                    self.user.pet['happiness'] = mood_
                    pet_file['happiness'] = mood_
                    dict_['BONE'] -= 1

                    print(f'Your pay: {food} - 15c')

                elif food == '3':
                    break
                else:
                    print('Invalid choice, try again!')

            ApplicationBIN.dump_to_bin(users)


app = ApplicationJSON()
app.run()

