import os
from Config import *
from Catalog import *

"""
Каталог книг
"""


class Interface:
    def __init__(self):
        """
        Проверим есть или нет настроки
        """
        if not os.path.exists('settings.ini'):
            """
            Если нет, - создадим
            """
            Config.create()
            config = Config()
            config.change_settings()
            Interface.create_catalog()
        else:
            """
            Если есть предложим изменить
            """
            config = Config()
            db_name = config.get_db_name()
            config.change_settings()
            print('Подключен каталог:', db_name)
            Interface.main_menu(db_name)

    def create_catalog():
        """
        Задаем имя каталога
        """
        valid = False
        catdir = 'base'
        while not valid:
            print("Существующие каталоги:")
            for file in os.listdir():
                if file.endswith(".db"):
                    print(os.path.join("", file))
            db_name = input("Введите название каталога\n")
            if db_name[-3:] != '.db':
                db_name = db_name + '.db'
            if os.path.exists(db_name) is False:
                print('Каталог с таким именем не существует',
                      '1 - создать каталог с таким именем',
                      '2 - выбрать другое имя',
                      '0 - выход', sep='\n')
                user_choice = int(input())
                if isinstance(user_choice, int):
                    pass
                else:
                    continue
                if user_choice == 1:
                    valid = True
                elif user_choice == 2:
                    continue
                elif user_choice == 0:
                    print('Выход из программы')
                    exit()
                else:
                    print("\nНекорректный ввод")
                    continue
            else:
                print('Подключен каталог:', db_name)
                valid = True
        config = Config()
        config.set_db_name(db_name)
        config.change_settings()
        Interface.main_menu(db_name)

    def main_menu(db_name):
        try:
            sql = Catalog(db_name)
            if not os.path.exists(db_name):
                sql.create()
            valid = False
            while not valid:
                print('Основное меню:',
                      '1 - подключить или создать другой каталог',
                      '2 - вывести содержимое каталога',
                      '3 - добавить книгу в каталог',
                      '4 - удалить книгу из каталога',
                      '5 - очистить каталог',
                      '6 - сохранить библиотеку в CSV формате',
                      '7 - сохранить библиотеку в JSON формате',
                      '0 - выход', sep='\n')
                main_choice = input()
                try:
                    main_choice = int(main_choice)
                except ValueError:
                    print("Некорректный ввод")
                    continue
                if main_choice == 1:
                    """
                    new
                    """
                    Interface.create_catalog()
                elif main_choice == 2:
                    """
                    print
                    """
                    sql.output()
                elif main_choice == 3:
                    book_name = input('Введите информацию о названии книги\n')
                    author = input('Введите информацию об авторе книги\n')
                    year_of_creation = input('Введите информацию об годе создания книги\n')
                    genre = input('Введите информацию о жанре книги\n')
                    book_data = [book_name, author, year_of_creation, genre]
                    sql.add_book(book_data)
                elif main_choice == 4:
                    search_input = input('Введите название книги для удаления из каталога\n')
                    sql.book_delete(search_input)
                elif main_choice == 5:
                    val_exit = False
                    while not val_exit:
                        user_conf = input("Это операция очистит каталог. Вы уверены? Да/Нет\n")
                        user_conf = user_conf.lower()
                        if user_conf == 'да':
                            sql.db_clear()
                            val_exit = True
                        elif user_conf == "нет":
                            val_exit = True
                        else:
                            print('Некорректный ввод')
                elif main_choice == 9:
                    filename_input = input('Введите название файла для сохранения в него каталога:\n')
                    sql.to_csv(filename_input)
                elif main_choice == 10:
                    filename_input = input('Введите название файла для сохранения в него каталога:\n')
                    sql.to_json(filename_input)
                elif main_choice == 0:
                    print('Завершение программы')
                    exit()
        except Exception as exc:
            pass


if __name__ == "__main__":
    Interface()