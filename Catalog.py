from prettytable import PrettyTable
from abc import ABC, abstractmethod
from driver import *


class Catalog:
    def __init__(self, db_name: str = None):
        self.db_name = str(db_name)

    def create(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE books (Название_книги text, autor  text, Год_выпуска text, Жанр text)""")
            conn.commit()
            conn.close()
            print('Каталог ', self.db_name, ' создан')
        except Exception as exc:
            print('Ошибка: Каталог не создан')

    def add_book(self, book: list):
        """
        Добавляем книгу в каталог.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            if type(book[0]) == list or type(book[0]) == tuple:
                book2 = []
                for i in book:
                    book2.append(tuple(map(lambda x: x.upper(), i)))
                book3 = []
                for i in book2:
                    book3.append(tuple(map(lambda x: x.strip(), i)))
                cursor.executemany("INSERT INTO books VALUES (?,?,?,?)", book3)
                conn.commit()
                conn.close()
                print('Книга успешно добавлена')
            elif type(book[0]) == str:
                book = list(map(lambda x: x.strip(), book))
                book = list(map(lambda x: x.upper(), book))
                book = [book]
                cursor.executemany("INSERT INTO books VALUES (?,?,?,?)", book)
                conn.commit()
                conn.close()
                print('Книга успешно добавлена')
        except Exception as exc:
            print('Что-то пошло не так')


    def output(self):
        """
        :return: Вывод библиотеки
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            sql = f'PRAGMA table_info(books)'
            cursor.execute(sql)
            row_names = ['№ строки']
            for i in cursor.fetchall():
                row_names.append(i[1])
            sql1 = f"SELECT * FROM books"
            cursor.execute(sql1)
            search_result = cursor.fetchall()
            new_result = []
            counter = 1
            for i in search_result:
                i = list(i)
                i.insert(0, counter)
                new_result.append(i)
                counter += 1
            table = PrettyTable(row_names)
            for i in new_result:
                table.add_row(i)
            print(table)
            conn.close()
            return search_result
        except Exception as exc:
            print('Что-то пошло не так')

    def book_delete(self, request: str = None):
        """
        Удаляем книгу из каталога
        """
        try:
            if request is None:
                print('Введите не пустое поле')
            else:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                aut = request
                cursor.execute("DELETE FROM books WHERE Название_книги = ?", (aut,))
                conn.commit()
                conn.close()
                print('Книга успешно удалена')
        except Exception as exc:
            print('Что-то пошло не так')

    def db_clear(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books')
            rez = cursor.fetchall()
            results = cursor.fetchall()
            print(results)
            conn.close()
            """
            Если все ок
            """
            print('Каталог очищен')
        except Exception as exc:
            """
            Если не все ок
            """
            print('Что-то пошло не так')



class DriverBuilder(ABC):
    @abstractmethod
    def build(self):
        pass


class JSONBuilder(DriverBuilder):
    def build(self):
        while True:
            filename = input('Введите имя для JSON файла: ')
            filename = filename.strip()
            if filename is None:
                break
            elif not filename.endswith('.json'):
                filename += '.json'
                trampampam = to_json(filename=filename)
                return trampampam


class CSVBuilder(DriverBuilder):
    def build(self):
        while True:
            filename = input('Введите имя для CSV файла: ')
            filename = filename.strip()
            if filename is None or filename == '':
                break
            elif not filename.endswith('.csv'):
                filename += '.csv'
                trampampam = to_csv(filename=filename)
                return trampampam


class FabricDriverBuilder():
    @staticmethod
    def get_driver():
        drivers = {
            1: JSONBuilder,
            2: CSVBuilder
        }
        for key, item in drivers.items():
            print(f'{key}:\t{item.__name__}')
        while True:
            driver_name = input('Enter Driver number or press [Enter] to quit: ')
            if driver_name is None or driver_name == '':
                return
            elif not driver_name.isdigit():
                print('Number must be int')
                continue
            else:
                driver_name = int(driver_name)
                break
        return drivers[driver_name]().build()

if __name__ == '__main__':
    avm = FabricDriverBuilder()
    print(avm.get_driver())
    pass
