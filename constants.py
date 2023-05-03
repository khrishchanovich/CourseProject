RULES = ('Вам предстоит не только выполнять ежедневные задачки'
'\nно и ухаживать за своим питомцем!'
'\nДля того, чтобы Ваш питомец был счастлив, нужно кормить его каждый день!'
'\nДля этого следуйте следующим правилам:'
'\n1) Ставьте перед собой ежедневные цели!'
'\n2) Выполняйте цели и получайте бонусы в виде монеток!'
'\n3) Покупайте за монетки корм для своего питомца в магазине!'
'\n4) Кормите питомца, играйте с ним и он обязательно будет счастлив!')

GREATING = ('Привет! Вы уже были тут раньше?')

def greating():
    print(GREATING)
    answer = input().lower()
    if answer == 'y':
        pass
        """load user"""
    if answer == 'n':
        pass
        """create new user"""



OPTIONS_TODO = """1 - add task
\n2 - edit task
\n3 - sort by status
\n4 - sort by category
\n5 - buy products
\n6 - info about your pet
\n7 - exit"""

OPTIONS_EDIT_TASK = """0 - response
\n1 - remove task
\n2 - change to DONE
\n3 - update"""

OPTIONS_UPDATE = """0 - response
\n1 - edit name
\n2 - edit category"""

CATEGORY = """NONE = 1
\nLEARNING = 2
\nWORKING = 3
\nPERSONAL = 4
\nTRAVELING = 5
\nDAILY = 6"""

GREETING = """Hello! Now you are currently using Gamify ToDo App!
\nPlease, enter your name and password!"""