import json
from filehandler import JSON

class Bonus:
    @staticmethod
    def add_coins(user, coins):
        user.coins += coins

        users = JSON.load_from_json()

        users[user.name]['coins'] += coins

        JSON.dump_to_json(users)

