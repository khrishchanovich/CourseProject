"""Class ToDoList"""

from entities.task import Task, Status, Category


class ToDoList:
    list_of_task: list[Task] = list()

    def add_to_do(self, task):
        self.list_of_task.append(task)

    def remove_to_do(self, index):
        self.list_of_task.pop(index)

    def set_to_do_list(self, tasks):
        self.list_of_task = tasks

    def get_to_do_list(self) -> list[Task]:
        return self.list_of_task

    def get_task_in_to_do(self, index: int, task) -> str:
        return task.set_title(self.list_of_task[index])

    def task_in_to_do(self, index: int):
        return self.list_of_task[index]

    def get_status_in_to_do(self, task) -> str:
        return task.get_status()

    def print_only_index_and_name(self):
        for i in self.list_of_task:
            print(f'{self.list_of_task.index(i) + 1}. {i.get_title()}: {i.get_status()}, {i.get_category()}')

    def sort_by_status(self):
        for i in self.list_of_task:
            if i.status == Status.DONE:
                print(f'{i.name}: {i.status}, {i.category}')

        for i in self.list_of_task:
            if i.status == Status.PENDING:
                print(f'{i.name}: {i.status}, {i.category}')

    def sort_by_category(self):
        for i in self.list_of_task:
            if i.category == Category.NONE:
                print(f'{i.name}: {i.status}, {i.category}')

        for i in self.list_of_task:
            if i.category == Category.LEARNING:
                print(f'{i.name}: {i.status}, {i.category}')

        for i in self.list_of_task:
            if i.category == Category.WORKING:
                print(f'{i.name}: {i.status}, {i.category}')

        for i in self.list_of_task:
            if i.category == Category.PERSONAL:
                print(f'{i.name}: {i.status}, {i.category}')

        for i in self.list_of_task:
            if i.category == Category.TRAVELING:
                print(f'{i.name}: {i.status}, {i.category}')

        for i in self.list_of_task:
            if i.category == Category.DAILY:
                print(f'{i.name}: {i.status}, {i.category}')

    def to_dict(self):
        task_dict = []
        for task in self.list_of_task:
            task_dict.append(task.to_dict())

        return task_dict

