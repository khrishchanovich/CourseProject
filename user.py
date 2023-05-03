from todolist import ToDoList


"""Class User"""


class User:

    def __init__(self, name, password, pet, coins, items):
        self.name = name
        self.password = password
        self.pet = pet
        self.coins = coins
        self.items = items
        self.todo = ToDoList()

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def to_dict(self):
        return {
            'name': self.name,
            'password': self.password,
            'pet': self.pet.to_dict(),
            'coins': self.coins,
            'items': self.items,
            'todo': self.todo.to_dict()
        }

