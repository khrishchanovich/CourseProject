from datetime import datetime
from enum import Enum

"""Class Status(Enum)"""


class Status(Enum):
    DONE = 'done'
    PENDING = 'pending'


"""Class Category(Enum)"""


class Category(Enum):
    NONE = 'none'
    LEARNING = 'learning'
    WORKING = 'working'
    PERSONAL = 'personal'
    TRAVELING = 'traveling'
    DAILY = 'daily'


"""Class Task"""


class Task:

    def __init__(self):
        self.name = ''
        self.status = Status.PENDING
        self.category = Category.NONE
        self.creation_time = datetime.utcnow()
        self.price = 15

    def __repr__(self):
        return f"{self.name} - status: {self.status.name}, category: {self.category.name}, price: {self.price}, " \
               f"created: {self.creation_time}"

    def to_dict(self):
        return {
                'name': self.name,
                'status': self.status.name,
                'category': self.category.name,
                'creation_time': self.creation_time.isoformat(),
                'price': self.price
        }

    def set_title(self, name):
        self.name = name

    def get_title(self):
        return self.name

    def set_status(self, complete):
        self.status = complete

    def get_status(self):
        return self.status

    def set_date_of_created(self, date):
        self.creation_time = date

    def get_date(self):
        return self.creation_time

    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price
