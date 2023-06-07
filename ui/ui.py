import tkinter
import datetime
import customtkinter
import sqlite3

from CTkMessagebox import CTkMessagebox

from entities.pet import Pet
from entities.animal import Type
from entities.user import User
from entities.task import Task, Category, Status
from entities.products import Products
from entities.storage import Storage

from utils.constants import Animal

from lib.filehandler import JSON


class AppUI:

    def __init__(self, master):
        self.master = master
        self.var_pet = customtkinter.StringVar(value='CAT')
        self.var_cat = customtkinter.StringVar(value='NONE')
        self.var_items = customtkinter.StringVar(value='FISH')
        self.string = str()

        self.login()

    def view_start(self):
        self.master.geometry('800x350')

        for i in self.master.winfo_children():
            i.destroy()

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users")
        rows = cursor.fetchall()

        self.list_of_names = []

        for row in rows:
            self.list_of_names.append(row[0])

        str_names = str()

        for i in self.list_of_names:
            str_names += f'''{i}\n'''

        users_lb = self.label_ctk(self.master, 'Список пользователей')
        users_lb.place(
            x=20,
            y=5
        )

        lst_box = self.lb_ctk(self.master)

        lst_box.place(
            x=10,
            y=35
        )

        lst_box.insert(1.0, str_names)
        lst_box.configure(state='disabled')

        lb_name = self.label_ctk(self.master, 'Имя: ')
        lb_name.place(
            x=500,
            y=45
        )

        self.entr_name = self.entry_ctk(self.master)
        self.entr_name.place(
            x=550,
            y=45
        )

        lb_psw = self.label_ctk(self.master, 'Пароль: ')
        lb_psw.place(
            x=475,
            y=85
        )

        self.entr_psw = self.entry_ctk(self.master)
        self.entr_psw.place(
            x=550,
            y=85
        )

    def login(self):
        self.view_start()

        self.master.geometry('800x250')

        lb_txt = self.label_ctk(self.master, 'Желаете войти?')
        lb_txt.place(
            x=565,
            y=5
        )

        btn_log = self.button_ctk(self.master, 'Войти', self.app_log)
        btn_log.place(
            x=550,
            y=150
        )

        btn_reg = self.button_ctk(self.master, 'Зарегистрироваться', self.register)
        btn_reg.place(
            x=543,
            y=200
        )

    def register(self):
        self.view_start()

        self.master.geometry('800x350')

        lb_txt = self.label_ctk(self.master, 'Регистрация')
        lb_txt.place(
            x=570,
            y=5
        )

        rd_cat = self.radio_ctk(
            self.master,
            'КОТ',
            'CAT',
            self.var_pet,
            self.set_type_of_pet
        )
        rd_cat.place(
            x=550,
            y=120
        )

        rd_dog = self.radio_ctk(
            self.master,
            'ПЕС',
            'DOG',
            self.var_pet,
            self.set_type_of_pet
        )
        rd_dog.place(
            x=550,
            y=160
        )

        lb_pet = self.label_ctk(self.master, 'Имя питомца: ')
        lb_pet.place(
            x=435,
            y=200
        )

        self.entr_pet = self.entry_ctk(self.master)
        self.entr_pet.place(
            x=550,
            y=200
        )

        self.pet = Pet(self.entr_pet.get())

        btn_reg = self.button_ctk(self.master, 'Зарегистрироваться', self.app_reg)
        btn_reg.place(
            x=545,
            y=250
        )

        btn_log = self.button_ctk(self.master, 'Войти', self.login)
        btn_log.place(
            x=555,
            y=300
        )

    def set_type_of_pet(self):
        if self.var_pet.get() == 'CAT':
            self.pet.set_type(Type.type_pet[1])
        elif self.var_pet.get() == 'DOG':
            self.pet.set_type(Type.type_pet[2])

    def string_view(self):
        string = str()

        for i in self.user.todo.list_of_task:
            string += f'{self.user.todo.list_of_task.index(i) + 1}. ' \
                      f'{i.get_title()}: ' \
                      f'\n{i.get_status().name}' \
                      f'\n{i.get_category().name}\n'

        self.list_box.destroy()
        self.scroll.destroy()

        self.list_box = self.lb_ctk(self.frame_list, 540)

        self.list_box.place(
            x=0,
            y=5
        )

        self.list_box.insert(1.0, string)
        self.list_box.configure(state='disabled')

    def frame_ctk(self, window, width=200, height=200):
        frame = customtkinter.CTkFrame(
            window,
            bg_color='LightCyan',
            fg_color='SteelBlue',
            width=width,
            height=height
        )

        return frame

    def scroll_ctk(self, window, command):
        scroll = customtkinter.CTkScrollbar(
            window,
            orientation='vertical',
            command=command,
            button_color='SteelBlue'
        )

        return scroll

    def lb_ctk(self, window, width=200):
        list_box = customtkinter.CTkTextbox(
            window,
            bg_color='LightCyan',
            fg_color='PaleTurquoise',
            font=('Helvetica', 15),
            activate_scrollbars=True,
            scrollbar_button_color='SteelBlue',
            width=width
        )

        return list_box

    def label_ctk(self, window, text, font=('Helvetica', 15), bc='LightCyan', fc='LightCyan', color='Black'):
        lb = customtkinter.CTkLabel(
            window,
            text=text,
            bg_color=bc,
            fg_color=fc,
            font=font,
            text_color=color
        )

        return lb

    def mb_ctk(self, title, message):
        msg = CTkMessagebox(title=title, message=message)

        return msg

    def entry_ctk(self, window, width=140):
        task_name = customtkinter.CTkEntry(
            window,
            bg_color='LightCyan',
            font=('Helvetica', 15),
            width=width
        )

        return task_name

    def button_ctk(self, window, text, command):
        button = customtkinter.CTkButton(
            window,
            text=text,
            bg_color='LightCyan',
            fg_color='SteelBlue',
            hover_color='RoyalBlue',
            font=('Helvetica', 15),
            text_color='Black',
            command=command
        )

        return button

    def radio_ctk(self, window, text, value, variable, command):
        radio = customtkinter.CTkRadioButton(
            window,
            text=text,
            value=value,
            bg_color='LightCyan',
            fg_color='SteelBlue',
            hover_color='RoyalBlue',
            font=('Helvetica', 15),
            variable=variable,
            command=command
        )

        return radio

    def add_window(self):
        window = tkinter.Tk()

        window.title('Добавление задачи')
        window.config(bg='LightCyan')
        window.geometry('500x200')

        lb = self.label_ctk(window, 'Введите имя задачи')
        lb.pack()

        self.entr_name_task = self.entry_ctk(window, 380)
        self.entr_name_task.pack()

        btn = self.button_ctk(window, 'Добавить', self.add_task)
        btn.pack()

        btn_close = self.button_ctk(window, 'Закрыть окно', lambda: window.destroy())
        btn_close.pack()

    def add_task(self):
        name = self.entr_name_task.get()

        new_task = Task()
        new_task.set_title(name)

        new_date = datetime.date.today()
        new_task.set_date_of_created(new_date)

        self.user.todo.add_to_do(new_task)

        users = JSON.load_from_json(self.user.name)

        list_ = [new_task.to_dict()]
        users['todo_task'] += list_

        JSON.dump_to_json(users, self.user.name)

        self.string_view()

    def remove_window(self):
        window = tkinter.Tk()

        window.title('Удаление задачи')
        window.config(bg='LightCyan')
        window.geometry('500x200')

        lb = self.label_ctk(window, 'Введите номер задачи')
        lb.pack()

        self.entr = self.entry_ctk(window)
        self.entr.pack()

        btn = self.button_ctk(window, 'Удалить', self.remove_task)
        btn.pack()

        btn_close = self.button_ctk(window, 'Закрыть окно', lambda: window.destroy())
        btn_close.pack()

    title = ['Ошибка', 'Предупреждение', 'Готово']

    def remove_task(self):
        if len(self.user.todo.get_to_do_list()) != 0:
            remove_by_number = int(self.entr.get())

            if remove_by_number != 0 and remove_by_number <= len(self.user.todo.get_to_do_list()):
                self.user.todo.remove_to_do(remove_by_number - 1)

                users = JSON.load_from_json(self.user.name)

                list_ = users['todo_task']
                del list_[remove_by_number - 1]
                users['todo_task'] = list_

                JSON.dump_to_json(users, self.user.name)

                self.string_view()

            elif remove_by_number > len(self.user.todo.get_to_do_list()):
                self.mb_ctk(self.title[0], 'Задачи под таким номером нет в списке.')
        else:
            self.mb_ctk(self.title[0], 'Ваш список пуст. Удалять нечего.')

    def status_window(self):
        window = tkinter.Tk()

        window.title('Изменить статус')
        window.config(bg='LightCyan')
        window.geometry('500x200')

        lb = self.label_ctk(window, 'Введите номер задачи')
        lb.pack()

        self.entr = self.entry_ctk(window)
        self.entr.pack()

        btn_status = self.button_ctk(window, 'Отметить как "DONE"', self.status_task)
        btn_status.pack()

        btn_close = self.button_ctk(window, 'Закрыть окно', lambda: window.destroy())
        btn_close.pack()

    def status_task(self):
        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            get_task_by_name = int(self.entr.get())
            if get_task_by_name != 0:
                searched = self.user.todo.task_in_to_do(get_task_by_name - 1)

                if searched.status != Status.DONE.name:
                    users = JSON.load_from_json(self.user.name)

                    list_ = users['todo_task']

                    for i in range(len(list_)):
                        if i == get_task_by_name - 1:
                            list_[i]['status'] = Status.DONE.name

                    users['coins'] += 15
                    self.user.coins += 15
                    JSON.dump_to_json(users, self.user.name)
                else:
                    self.mb_ctk(self.title[0], 'Эта задача уже выполнена.')
            else:
                self.mb_ctk(self.title[0], 'Такой задачи не существует.')

            if searched.status != Status.DONE:
                searched.set_status(Status.DONE)
                self.mb_ctk(self.title[2], 'Вы выполнили поставленную задачу.')

                self.lb_coins.configure(text='Монеты: ' + str(self.user.coins))

            self.string_view()

    def set_type_of_cat(self):
        number = self.task_category.get()

        if self.var_cat.get() == 'NONE':
            self.user.todo.list_of_task[int(number) - 1].set_category(Category.NONE)
        elif self.var_cat.get() == 'LEARNING':
            self.user.todo.list_of_task[int(number) - 1].set_category(Category.LEARNING)
        elif self.var_cat.get() == 'WORKING':
            self.user.todo.list_of_task[int(number) - 1].set_category(Category.WORKING)
        elif self.var_cat.get() == 'PERSONAL':
            self.user.todo.list_of_task[int(number) - 1].set_category(Category.PERSONAL)
        elif self.var_cat.get() == 'TRAVELING':
            self.user.todo.list_of_task[int(number) - 1].set_category(Category.TRAVELING)
        elif self.var_cat.get() == 'DAILY':
            self.user.todo.list_of_task[int(number) - 1].set_category(Category.DAILY)

    def category_window(self):
        window = tkinter.Tk()

        number = self.task_category.get()

        if number == '' or number.isalpha():
            window.destroy()

        window.title('Изменить категорию')
        window.config(bg='LightCyan')
        window.geometry('500x500')

        rd_none = self.radio_ctk(
            window,
            'Без категории',
            'NONE',
            self.var_cat,
            self.set_type_of_cat
        )
        rd_none.place(
            x=125,
            y=25
        )

        rd_learning = self.radio_ctk(
            window,
            'Учеба',
            'LEARNING',
            self.var_cat,
            self.set_type_of_cat
        )
        rd_learning.place(
            x=125,
            y=65
        )

        rd_working = self.radio_ctk(
            window,
            'Работа',
            'WORKING',
            self.var_cat,
            self.set_type_of_cat
        )
        rd_working.place(
            x=125,
            y=105
        )

        rd_personal = self.radio_ctk(
            window,
            'Личное',
            'PERSONAL',
            self.var_cat,
            self.set_type_of_cat
        )
        rd_personal.place(
            x=125,
            y=145
        )

        rd_traveling = self.radio_ctk(
            window,
            'Путешествия',
            'TRAVELING',
            self.var_cat,
            self.set_type_of_cat
        )
        rd_traveling.place(
            x=125,
            y=185
        )

        rd_daily = self.radio_ctk(
            window,
            'Ежедневное',
            'DAILY',
            self.var_cat,
            self.set_type_of_cat
        )
        rd_daily.place(
            x=125,
            y=225
        )

        btn = self.button_ctk(window, 'Изменить категорию', self.category_task)
        btn.place(
            x=125,
            y=265
        )

        btn_close = self.button_ctk(window, 'Закрыть окно', lambda: window.destroy())
        btn_close.place(
            x=127,
            y=305
        )

    def category_task(self):
        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            get_task_by_name = int(self.task_category.get())
            if get_task_by_name != 0:
                searched = self.user.todo.task_in_to_do(get_task_by_name - 1)

                print(searched)

                print(self.var_cat)

                if self.var_cat.get() == 'NONE':
                    searched.set_category(Category.NONE)
                    users = JSON.load_from_json(self.user.name)

                    list_ = users['todo_task']

                    for i in range(len(list_)):
                        if i == get_task_by_name - 1:
                            list_[i]['category'] = Category.NONE.name

                    JSON.dump_to_json(users, self.user.name)

                elif self.var_cat.get() == 'LEARNING':
                    searched.set_category(Category.LEARNING)
                    users = JSON.load_from_json(self.user.name)

                    list_ = users['todo_task']

                    for i in range(len(list_)):
                        if i == get_task_by_name - 1:
                            list_[i]['category'] = Category.LEARNING.name

                    JSON.dump_to_json(users, self.user.name)

                elif self.var_cat.get() == 'WORKING':
                    searched.set_category(Category.WORKING)
                    users = JSON.load_from_json(self.user.name)

                    list_ = users['todo_task']

                    for i in range(len(list_)):
                        if i == get_task_by_name - 1:
                            list_[i]['category'] = Category.WORKING.name

                    JSON.dump_to_json(users, self.user.name)

                elif self.var_cat.get() == 'PERSONAL':
                    searched.set_category(Category.PERSONAL)
                    users = JSON.load_from_json(self.user.name)

                    list_ = users['todo_task']

                    for i in range(len(list_)):
                        if i == get_task_by_name - 1:
                            list_[i]['category'] = Category.PERSONAL.name

                    JSON.dump_to_json(users, self.user.name)

                elif self.var_cat.get() == 'TRAVELING':
                    searched.set_category(Category.TRAVELING)
                    users = JSON.load_from_json(self.user.name)

                    list_ = users['todo_task']

                    for i in range(len(list_)):
                        if i == get_task_by_name - 1:
                            list_[i]['category'] = Category.TRAVELING.name

                    JSON.dump_to_json(users, self.user.name)

                elif self.var_cat.get() == 'DAILY':
                    searched.set_category(Category.DAILY)
                    users = JSON.load_from_json(self.user.name)

                    list_ = users['todo_task']

                    for i in range(len(list_)):
                        if i == get_task_by_name - 1:
                            list_[i]['category'] = Category.DAILY.name

                    JSON.dump_to_json(users, self.user.name)

            self.mb_ctk(self.title[2], 'Вы изменили категорию задачи')

            self.string_view()

    def new_window(self):
        window = tkinter.Tk()

        window.title('Изменение имени')
        window.config(bg='LightCyan')
        window.geometry('500x200')

        lb_number = self.label_ctk(window, 'Введите номер задачи')
        lb_number.pack()

        self.entr = self.entry_ctk(window)
        self.entr.pack()

        lb_name = self.label_ctk(window, 'Введите новое имя')
        lb_name.pack()

        self.entr_name = self.entry_ctk(window, 380)
        self.entr_name.pack()

        btn = self.button_ctk(window, 'Изменить', self.new_task)
        btn.pack()

        btn_close = self.button_ctk(window, 'Закрыть окно', lambda: window.destroy())
        btn_close.pack()

    def new_task(self):
        searched = Task()

        if len(self.user.todo.get_to_do_list()) != 0:
            get_title_by_number = int(self.entr.get())

            if get_title_by_number != 0:
                searched = self.user.todo.task_in_to_do(get_title_by_number - 1)

            users = JSON.load_from_json(self.user.name)

            list_ = users['todo_task']

            for i in range(len(list_)):
                if i == get_title_by_number - 1:
                    list_[i]['name'] = self.entr_name.get()

            JSON.dump_to_json(users, self.user.name)
            searched.set_title(self.entr_name.get())

            self.string_view()

            self.mb_ctk(self.title[2], 'Задача изменена.')
        else:
            self.mb_ctk(self.title[0], 'Список задач пуст.')

    def set_type_of_item(self):
        if self.var_items.get() == 'FISH':
            self.user.items['FISH'] += 1
        elif self.var_items.get() == 'BONE':
            self.user.items['BONE'] += 1

    def buy_window(self):
        self.window = tkinter.Tk()

        self.window.title('Магазин')
        self.window.config(bg='LightCyan')
        self.window.geometry('500x300')

        store = Storage()

        lb_inv = self.label_ctk(self.window, 'Ваш инвентарь')
        lb_inv.pack()

        self.lb_fish = self.label_ctk(self.window, 'Количество рыбки: ' + str(self.user.items['FISH']))
        self.lb_fish.pack()

        self.lb_bone = self.label_ctk(self.window, 'Количество косточек: ' + str(self.user.items['BONE']))
        self.lb_bone.pack()

        lb = self.label_ctk(self.window, 'Магазин')
        lb.pack()

        rd_fish = self.radio_ctk(
            self.window,
            'Рыбка',
            store.get_items()[0],
            self.var_items,
            self.var_items.get
        )
        rd_fish.pack()

        rd_bone = self.radio_ctk(
            self.window,
            'Косточка',
            store.get_items()[1],
            self.var_items,
            self.var_items.get
        )
        rd_bone.pack()

        btn = self.button_ctk(self.window, 'Купить', self.buy_item)
        btn.pack()

        btn_close = self.button_ctk(self.window, 'Закрыть окно', lambda: self.window.destroy())
        btn_close.pack()

    def buy_item(self):
        Products.buy_json(self.user, self.var_items.get())

        self.lb_fish.configure(text='Количество рыбки: ' + str(self.user.items['FISH']))
        self.lb_bone.configure(text='Количество косточек: ' + str(self.user.items['BONE']))
        self.lb_coins.configure(text='Монеты: ' + str(self.user.coins))

    def info_pet(self, name):
        self.check()
        users = JSON.load_from_json(name)

        pet_ = users['pet']

        lb_petname = self.label_ctk(self.master, pet_['name'], ('Helvetica', 30))
        lb_petname.place(
            x=5,
            y=295
        )

        life = str()

        if 75 < pet_['happiness'] <= 100:
            life = '\u2665\u2665\u2665\u2665'
        elif 50 < pet_['happiness'] <= 75:
            life = '\u2665\u2665\u2665\u2661'
        elif 25 < pet_['happiness'] <= 50:
            life = '\u2665\u2665\u2661\u2661'
        elif 0 <= pet_['happiness'] <= 25:
            life = '\u2665\u2661\u2661\u2661'

        lb_happiness = self.label_ctk(self.master, life, color='Red', font=('Helvetica', 30))
        lb_happiness.place(
            x=5,
            y=325
        )

    def info_about_pet(self):
        users = JSON.load_from_json(self.user.name)

        pet_file = users['pet']

        name = pet_file['name']
        type = pet_file['type']
        mood = pet_file['happiness']
        date = pet_file['date']

        pet_ = Pet(name)

        pet_.set_type(type)
        pet_.set_mood(mood)
        pet_.set_age(datetime.datetime.strptime(date, '%Y-%m-%d').date())

        return pet_

    def info_about_coins(self, name):
        users = JSON.load_from_json(name)

        self.lb_coins = self.label_ctk(self.master, 'Монеты: ' + str(users['coins']))
        self.lb_coins.place(
            x=5,
            y=50
        )

    def check(self):
        pet_ = self.info_about_pet()

        mood = pet_.check_mood()

        users = JSON.load_from_json(self.user.name)

        dict_ = users['pet']

        dict_['happiness'] = mood
        dict_['date'] = datetime.date.today().isoformat()

        JSON.dump_to_json(users, self.user.name)

    def set_feed_item(self):
        if self.var_items.get() == 'FISH':
            self.user.items['FISH'] -= 1
        elif self.var_items.get() == 'BONE':
            self.user.items['BONE'] -= 1

    def feed_window(self):
        window = tkinter.Tk()

        window.title('Время обеда')
        window.config(bg='LightCyan')
        window.geometry('500x300')

        store = Storage()

        lb = self.label_ctk(window, 'Покормите питомца')
        lb.pack()

        self.lb_fish_ = self.label_ctk(window, 'Количество рыбки: ' + str(self.user.items['FISH']))
        self.lb_fish_.pack()

        self.lb_bone_ = self.label_ctk(window, 'Количество косточек: ' + str(self.user.items['BONE']))
        self.lb_bone_.pack()

        rd_fish = self.radio_ctk(
            window,
            'Рыбка',
            store.get_items()[0],
            self.var_items,
            self.set_feed_item
        )
        rd_fish.pack()

        rd_bone = self.radio_ctk(
            window,
            'Косточка',
            store.get_items()[1],
            self.var_items,
            self.set_feed_item
        )
        rd_bone.pack()

        btn = self.button_ctk(window, 'Покормить', self.feed_pet)
        btn.pack()

        btn_close = self.button_ctk(window, 'Закрыть окно', lambda: window.destroy())
        btn_close.pack()

    def feed_pet(self):
        self.check()
        pet_ = self.info_about_pet()

        users = JSON.load_from_json(self.user.name)

        dict_ = users['items']
        pet_file = users['pet']

        if dict_['FISH'] == 0 and dict_['BONE'] == 0:
            self.mb_ctk(self.title[1], 'В вашем инвентаре ничего нет.')

        if dict_['FISH'] > 0:
            if self.var_items.get() == 'FISH':
                mood_ = pet_.feed('FISH')

                self.user.pet['happiness'] = mood_
                pet_file['happiness'] = mood_
                dict_['FISH'] -= 1

        if dict_['BONE'] > 0:
            if self.var_items.get() == 'BONE':
                mood_ = pet_.feed('BONE')

                self.user.pet['happiness'] = mood_
                pet_file['happiness'] = mood_
                dict_['BONE'] -= 1

        self.user.items = users['items']
        self.user.coins = users['coins']

        JSON.dump_to_json(users, self.user.name)

        self.lb_fish_.configure(text='Количество рыбки: ' + str(self.user.items['FISH']))
        self.lb_bone_.configure(text='Количество косточек: ' + str(self.user.items['BONE']))

        self.info_pet(self.user.name)

    def app(self, string, name):
        lb_name = self.label_ctk(self.master, 'Пользователь ' + name, font=('Segoe UI Semibold', 20))
        lb_name.place(
            x=5,
            y=5
        )

        self.frame_pet = self.frame_ctk(self.master)
        self.frame_pet.place(
            x=5,
            y=95
        )

        lb_task = self.label_ctk(self.master, 'Ваши задачи: ')
        lb_task.place(
            x=420,
            y=5
        )

        self.frame_list = self.frame_ctk(self.master, 520)
        self.frame_list.place(
            x=250,
            y=50
        )

        self.list_box = self.lb_ctk(self.frame_list, 540)

        self.scroll = self.scroll_ctk(self.list_box, self.list_box.yview)

        self.list_box.configure(yscrollcommand=self.scroll.set)

        self.scroll.place(
            x=500,
            y=5
        )
        self.list_box.place(
            x=0,
            y=5
        )

        self.list_box.insert(1.0, string)
        self.list_box.configure(state='disabled')

        lb_task_edit = self.label_ctk(self.master, 'Задача: ')
        lb_task_edit.place(
            x=630,
            y=265
        )

        btn_add = self.button_ctk(self.master, 'Добавить', self.add_window)
        btn_add.place(
            x=630,
            y=300
        )

        btn_del = self.button_ctk(self.master, 'Удалить', self.remove_window)
        btn_del.place(
            x=630,
            y=330
        )

        lb_edit = self.label_ctk(self.master, 'Изменить')
        lb_edit.place(
            x=630,
            y=370
        )

        btn_status = self.button_ctk(self.master, 'Статус', self.status_window)
        btn_status.place(
            x=630,
            y=405
        )

        lb_number = self.label_ctk(self.master, 'Номер задачи: ')
        lb_number.place(
            x=480,
            y=435
        )

        btn_category = self.button_ctk(self.master, 'Категория', self.category_window)
        btn_category.place(
            x=630,
            y=465
        )

        self.task_category = self.entry_ctk(self.master)
        self.task_category.place(
            x=480,
            y=465
        )

        btn_name = self.button_ctk(self.master, 'Имя', self.new_window)
        btn_name.place(
            x=630,
            y=495
        )

        btn_store = self.button_ctk(self.master, 'Купить', self.buy_window)
        btn_store.place(
            x=5,
            y=400
        )

        btn_feed = self.button_ctk(self.master, 'Покормить', self.feed_window)
        btn_feed.place(
            x=5,
            y=430
        )

    def app_log(self):
        text_name = self.entr_name.get()
        text_password = self.entr_psw.get()

        for i in self.master.winfo_children():
            i.destroy()

        self.master.geometry('800x600')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('SELECT password FROM users WHERE username=?', (text_name,))
        password = cursor.fetchone()

        if text_name not in self.list_of_names:
            self.login()
            self.mb_ctk(self.title[0], 'Пользователя не существует в списке. Зарегистрируйтесь.')

        elif text_name in self.list_of_names and password[0] != text_password:
            self.login()
            self.mb_ctk(self.title[0], 'Неверный пароль.')

        else:
            if len(text_name) == 0 or len(text_password) == 0:
                self.mb_ctk(self.title[0], 'Пропущен один из параметров.')

            elif len(text_name) != 0 and len(text_password) != 0:
                if len(text_name) > 20:
                    self.login()
                    self.mb_ctk(self.title[0], 'Имя не должно превышать 20 символов.')

                elif len(text_password) < 8:
                    self.login()
                    self.mb_ctk(self.title[0], 'Пароль должен превышать 8 символов.')

                else:
                    string = str()

                    if text_name in self.list_of_names and password[0] == text_password:
                        users = JSON.load_from_json(text_name)

                        coins = users['coins']
                        items = users['items']
                        pet = users['pet']

                        self.user = User(text_name, text_password, pet, coins, items)
                        list_ = users['todo_task']

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

                        for i in self.user.todo.list_of_task:
                            string += f'{self.user.todo.list_of_task.index(i) + 1}. ' \
                                      f'{i.get_title()}: ' \
                                      f'\n{i.get_status().name}' \
                                      f'\n{i.get_category().name}\n'

                        pet_ = users['pet']

                        self.app(string, text_name)

                        if pet_['type'] == 'CAT':
                            lb_pet = self.label_ctk(self.frame_pet, Animal.CAT, ('Segoe UI Semibold', 20),
                                                    bc='LightCyan',
                                                    fc='SteelBlue')
                            lb_pet.place(
                                x=50,
                                y=25
                            )

                        elif pet_['type'] == 'DOG':
                            lb_pet = self.label_ctk(self.frame_pet, Animal.DOG, ('Segoe UI Semibold', 20),
                                                    bc='LightCyan',
                                                    fc='SteelBlue')
                            lb_pet.place(
                                x=50,
                                y=25
                            )

                        self.info_pet(self.user.name)
                        self.info_about_coins(self.user.name)

    def app_reg(self):
        text_name_reg = self.entr_name.get()
        text_password = self.entr_psw.get()

        text_name_pet = self.entr_pet.get()

        for i in self.master.winfo_children():
            i.destroy()

        self.master.geometry('800x600')

        if text_name_reg in self.list_of_names:
            self.register()
            self.mb_ctk(self.title[0], 'Пользователь уже существует')

        else:
            if len(text_name_reg) == 0 or len(text_password) == 0 or len(text_name_pet) == 0:
                self.register()
                self.mb_ctk(self.title[0], 'Пропущен один из параметрова. Повторите попытку.')

            elif len(text_name_reg) != 0 and len(text_password) != 0 and len(text_name_reg) != 0:
                if len(text_name_reg) > 20:
                    self.register()
                    self.mb_ctk(self.title[0], 'Имя не должно превышать 20 символов.')

                elif len(text_name_pet) > 20:
                    self.register()
                    self.mb_ctk(self.title[0], 'Имя питомца не должно превышать 20 символов.')

                elif len(text_password) < 8:
                    self.register()
                    self.mb_ctk(self.title[0], 'Пароль должен превышать 8 символов.')

                else:
                    conn = sqlite3.connect('../ui/users.db')
                    c = conn.cursor()

                    c.execute('''CREATE TABLE IF NOT EXISTS users
                                         (username TEXT PRIMARY KEY, password TEXT)''')

                    c.execute('INSERT INTO users VALUES (?, ?)', (text_name_reg, text_password))

                    conn.commit()
                    conn.close()

                    self.app('', text_name_reg)

                    pet_ = Pet(text_name_pet)

                    if self.var_pet.get() == 'CAT':
                        lb_pet = self.label_ctk(self.frame_pet, Animal.CAT, ('Segoe UI Semibold', 20), bc='LightPink',
                                                fc='LightPink')
                        lb_pet.place(
                            x=50,
                            y=25
                        )
                        pet_.set_type(Type.type_pet[1])

                    elif self.var_pet.get() == 'DOG':
                        lb_pet = self.label_ctk(self.frame_pet, Animal.DOG, ('Segoe UI Semibold', 20), bc='LightPink',
                                                fc='LightPink')
                        lb_pet.place(
                            x=50,
                            y=25
                        )
                        pet_.set_type(Type.type_pet[2])

                    self.user = User(text_name_reg, text_password, pet_, 15, {})

                    with open(f"users/{text_name_reg}.json", "w") as fw:
                        pass

                    with open(f"users/{text_name_reg}.json", "w") as fw:
                        users = {'pet': pet_.to_dict(), 'coins': 15, 'items': {'FISH': 0, 'BONE': 0}, 'todo_task': []}
                        JSON.dump_to_json(users, text_name_reg)

                    self.info_pet(self.user.name)
                    self.info_about_coins(self.user.name)

root = customtkinter.CTk()
root.config(bg='LightCyan')
AppUI(root)
root.mainloop()
