from threading import Thread
from time import sleep
from random import randint
import queue


class Table:
    number = 0
    guest = None

    def __init__(self, number):
        self.number = number


class Guest(Thread):
    name = ""

    def __init__(self, name):
        self.name = name
        super().__init__()

    def run(self):
        sleep(randint(3,10))

class Cafe:
    q = queue.Queue()
    tables = []

    def __init__(self, *args):
        for t in args:
            self.tables.append(t)

    def guest_arrival(self, *guests):
        for guest in guests:
            flag = False
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    flag = True
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    break
            if not flag:
                self.q.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        tables_reserved = ["0" if table.guest is None else "1" for table in self.tables]
        while not self.q.empty() or "1" in tables_reserved:
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None
                    tables_reserved[table.number-1] = "0"
                if not self.q.empty() and "0" in tables_reserved:
                    guest_ = self.q.get()
                    table_ = self.tables[tables_reserved.index("0")]
                    table_.guest = guest_
                    tables_reserved[tables_reserved.index("0")] = "1"
                    print(f"{guest_.name} вышел(-ла) из очереди и сел(-а) за стол номер { table_.number}")
                    guest_.start()
                    guest_.join()


tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()