from datetime import datetime

"""Class Animal"""

class Type:
    type_pet = ['NONE', 'CAT', 'DOG']


class Animal:

    def __init__(self, name, mood=100):
        self.type = Type.type_pet
        self.mood = mood
        self.name = name
        self.created_date = datetime.utcnow().date()

    def __repr__(self):
        return f'{self.type}, mood: {self.mood}'

    def set_mood(self, mood):
        self.mood = mood

    def get_mood(self):
        return self.mood

    def set_age(self, date):
        self.created_date = date

    def get_age(self):
        return self.created_date


