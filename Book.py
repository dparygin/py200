class Book:
    """
    Создание записи о книге
    """
    @staticmethod
    def book_create(book_data: list or tuple = None):
        if book_data is None:
            book_name = input('Введите информацию о названии книги\n')
            author = input('Введите информацию об авторе книги\n')
            year_of_creation = input('Введите информацию об годе создания книги\n')
            genre = input('Введите информацию о жанре книги\n')
            book_data = [book_name, author, year_of_creation, genre]
        writer = Catalog()

    """
    Удаление записи
    """
    @staticmethod
    def book_delete(filename: str):
        try:
            os.path.isfile(filename)
            os.remove(filename)
            print("Файл успешно удален")
        except Exception as exc:
            print("Файл не найден")
