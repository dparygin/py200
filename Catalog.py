import sqlite3
from prettytable import PrettyTable
import csv
import json


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

    def to_csv(self, filename: str = None, book: list = None):
        if len(filename) == 0:
            filename = 'output.csv'
        else:
            if filename[-4:] != '.csv':
                filename = filename + '.csv'
        try:
            if book is None:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM books")
                with open(filename, 'x', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow([i[0] for i in cursor.description])
                    for result in cursor:
                        writer.writerow(result)
                conn.close()
                print('CSV-файл успешно сохранен')
            else:
                with open(filename, 'x', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(book)
                    print('CSV-файл успешно сохранен')
        except FileExistsError:
            print('Файл с таким названием уже существует\n')

    def to_json(self, filename: str = 'output.csv', book: list = None):
        if len(filename) == 0:
            filename = 'output.json'
        else:
            if filename[-5:] != '.json':
                filename = filename + '.json'
        try:
            if book is None:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM books")
                result = cursor.fetchall()
                with open(filename, 'x', newline='') as file:
                    json.dump(result, file)
                conn.close()
                print('JSON-файл успешно сохранен')
            else:
                with open(filename, 'x', newline='') as file:
                    json.dump(book, file)
                    print('JSON-файл успешно сохранен')
        except FileExistsError:
            print('Файл с таким названием уже существует\n')
