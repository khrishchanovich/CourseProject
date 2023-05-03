import datetime
import json

from animal import Animal
from storage import Storage


class Pet(Animal):

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'happiness': self.mood,
            'date': self.created_date.isoformat()
        }

    def from_dict(self, cls, pet_dict: dict):
        return cls(pet_dict['name'], pet_dict['type'], pet_dict['happiness'], pet_dict['date'])


    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def feed(self, food, store=Storage()):
        if food == store.get_items()[0] and self.type[1]:
            self.mood += 20
        elif food == store.get_items()[1] and self.type[2]:
            self.mood += 20
        else:
            self.mood += 10
        self.mood = min(self.mood, 100)

        return self.mood

    def check_mood(self):
        days_since_birth = (datetime.date.today() - self.created_date).days
        self.mood = max(0, self.mood - (days_since_birth * 25))

        return self.mood


